# External Security Review — reanchor launcher template — Claude Opus 5 — 2026-08-27

**Verdict**: ADMIT IN PART

The nine pre-candidate steps are all present in
`bootstrap/reanchor-launcher.template.sh`, in the order the registry claims, and
their logic is sound. I admit the file's *text* at the digest recorded below.

What I do **not** admit is the sentence the ceremony's own documents write about
these bytes. Two stated properties are false as written, and I proved both by
running them:

1. **RA-01's "recorded" is not delivered.** The launcher's values reader tests
   whether a variable is *set*, not whether the values file set it. An exported
   `L_shasum` therefore satisfies the "missing required key" refusal, and the
   environment-supplied program **executes** — I watched it hash the packet. The
   pre-candidate digest tool can come from the ambient environment. That is the
   exact failure `bootstrap/SAFETY.md` Rule 13 says this design exists to
   remove, reached through a channel nobody closed.
2. **Nothing mechanical binds the launcher the operator runs to the launcher a
   review read.** Not the closure, not the gate manifest, not the artifact. The
   only binding is a human comparing two hex strings, one of which lives in a
   document delivered out of band.

So: reviewing this file clears less than it appears to, and the prior review was
right to withhold. Details and commands below.

### Findings at a glance

| id | what it is | severity |
|---|---|---|
| **L-1** | an exported `L_<key>` satisfies the launcher's required-key check and the injected executable runs — "no ambient fallback" is false for the variable-name channel | **fix before the next ceremony** |
| **L-2** | nothing in the repository binds the instantiated launcher to the reviewed template; the binding is one human digest comparison | structural; state it, do not paper over it |
| **L-3** | the launcher is outside the authority closure it verifies, and performs 9 of the registry's 19 steps | structural; confirmed independently |
| **L-4** | the `+10` delta is presentation-only and does not touch the two-stage boundary; but `CAIRN_LAUNCHER=$0` is not canonicalised, so the printed command can be relative | low |
| **L-5** | the re-extraction property is real **only** on the launcher's `--stage2` path; the runbook and `reanchor.sh steps` both still attribute it to `stage2` | fix before next ceremony (confirms and sharpens prior R-1) |
| **L-6** | `--stage2 ''` silently runs **stage 1** | low; fails closed after RA-16 |
| **L-7** | `|| ANCHORED=''` at `:577-578` is unreachable — pipeline status is `shasum`'s | dead guard; safe direction |
| **L-8** | `MAX_PACKET_BYTES` is declared and never used; the packet has no whole-file bound | trivial |
| **L-9** | no `trap`; a `die` after `mktemp` leaves `$T` behind, and stage 1's `$T` (holding candidate code) is never removed | hygiene |
| **L-10** | *(out of scope, observed)* the identical injection exists in `bootstrap/reanchor.sh` at `V_*` and reaches `V_python`, the interpreter that runs the checker | **report to the Maintainer** |

---

## Range and identity

| | value |
|---|---|
| file | `bootstrap/reanchor-launcher.template.sh`, 648 lines |
| sha256 at `HEAD` (`da58925`) | `9063e7d626e5ec15624ed9d81a8151915b69eb0c664420f585ef797ad55d2c5d` |
| git blob at `HEAD` | `4eba8cfb1e9df29cb8de3f78878a37eaeee997ab` |
| sha256 at `refs/cairn/gate-anchor` (`5f99273`) | `2d3e0f991c131b352df7d269f0762bd5def514a26c26ada077e6117d4454ac39` |
| git blob at anchor | `b8ea33d8a7d2ff41cdf847334e460b9d92dbb77b` |
| delta | `+10 / −0`, one hunk, commit `d091cdd` |

Working tree clean of tracked changes at review time (`git status --short`
reported only untracked `.claude/` and `dev/measurement/collision_log.md`).

**A note on what a digest here can mean.** For the other closure members, a
recorded sha256 is checkable by machinery: `check_authority_modules` in
`bootstrap/tests/_gate_preflight.py` compares live bytes against the admitted
digest. For *this* file there is no such comparison anywhere — see L-2 and L-3.
The digest above is a coordinate for a human, not an input to a check.

---

## The two framing facts, verified rather than accepted

```
$ grep -c 'reanchor-launcher' bootstrap/reanchor.sh
0
```

```
$ PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -c "
import sys; sys.path.insert(0,'bootstrap/tests')
import _gate_preflight as P
print('TEMPLATE IN CLOSURE:', 'bootstrap/reanchor-launcher.template.sh'
      in P.declared_authority_closure())"
TEMPLATE IN CLOSURE: False
```

I also checked the *other* integrity mechanism, which the prior review did not
have to:

```
$ PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -c "
import sys; sys.path.insert(0,'bootstrap/tests')
import _gate_manifest as G
f = G._frozen_files()
print('frozen count', len(f))
print('TEMPLATE FROZEN:', 'bootstrap/reanchor-launcher.template.sh' in f)"
frozen count 181
TEMPLATE FROZEN: False
```

The frozen surface is globbed at `bootstrap/tests/_gate_manifest.py:351-353` as
`bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`,
`scripts/*.py`, `templates/modules/**/*.py`. No `.sh` glob under `bootstrap/`.
The launcher template is a shell file at `bootstrap/`, so it falls through every
pattern.

**Net: the file that performs nine of the nineteen ceremony steps is covered by
neither the authority closure nor the frozen gate surface, and the artifact it
starts does not know its name.**

---

## L-1 — the environment can supply a pre-candidate executable *(headline)*

### The claim being tested

Three documents state the same property, in escalating language.

`bootstrap/reanchor-launcher.template.sh:212` —
`# NO AMBIENT FALLBACK. Absent means refuse, never "find it on PATH".`

`bootstrap/reanchor-values.example:15-17` — the grammar promises "no ambient
fallback **of any kind** — an absent field refuses rather than being filled from
PATH, HOME or Git config".

`bootstrap/SAFETY.md:606-613`, Rule 13, is the load-bearing one:

> every executable is an **absolute path recorded by the Maintainer in the
> values file** … Ambient discovery is the failure this design exists to remove:
> it is what once let a substituted repository answer for the named one, and a
> replacement `shasum` vouch for bytes it had just rewritten.

### The mechanism

`read_values` at `bootstrap/reanchor-launcher.template.sh:151-230` never
initialises its seven output variables. It uses `${L_git+s}` — *is this variable
set* — for both the duplicate check (`:194-209`) and the required-key check
(`:212-219`). A shell variable inherited from the environment is set. So:

* if the values file **names** the key, an exported `L_git` makes it die
  `duplicate key 'git'` — fail-closed, and this is why the hole is not
  immediately obvious;
* if the values file **omits** the key, the environment silently supplies it,
  and the only remaining checks are absoluteness, symlink-freedom, regular-file
  and the executable bit — all of which an attacker-planted binary satisfies.

The asymmetry inside this same file is what tells me this is an oversight rather
than a decision: `parse_packet` at `:303-310` explicitly zeroes every `P_*`
before parsing, and `STAGE2_CONFIRM` (`:435`) and `CLOSURE_CHANGED` (`:573`) are
initialised too. `read_values` is the one reader that is not.

### Evidence — the required-key refusal, defeated

Positive control first, so the absence I report is an absence that *could* have
been present. Values file with all seven keys, run against the unfilled
template — reaches the packet-digest refusal, which is downstream of
`read_values`:

```
$ sh bootstrap/reanchor-launcher.template.sh $LAB/packet.txt $LAB/vals_full.txt HEAD
REFUSE: this launcher's embedded packet digest is not 64 hex characters
('@PACKET_SHA256@'). An UNFILLED TEMPLATE is not an operative launcher: …
exit=1
```

Same values file with `git` removed, clean environment — the refusal fires:

```
$ env -u L_git sh bootstrap/reanchor-launcher.template.sh \
      $LAB/packet.txt $LAB/vals_nogit.txt HEAD
REFUSE: values file: missing required key 'git'
exit=1
```

Same values file, same command, one exported variable:

```
$ L_git=/bin/echo sh bootstrap/reanchor-launcher.template.sh \
      $LAB/packet.txt $LAB/vals_nogit.txt HEAD
REFUSE: this launcher's embedded packet digest is not 64 hex characters …
exit=1
```

The refusal is gone. `read_values` completed with a `git` the values file never
named.

### Evidence — the injected executable *runs*, in the pre-candidate window

The refusal above proves the check was bypassed. It does not prove use. To prove
use I copied the template into a scratchpad (I did **not** edit the repository
file), filled `@PACKET_SHA256@` with the sha256 of my throwaway packet, and
pointed `L_shasum` at a wrapper that announces itself and then delegates to the
real `/usr/bin/shasum`.

Control — values file omits `shasum`, clean environment:

```
$ sh ./inst.sh $LAB/packet.txt $LAB/vals_noshasum.txt HEAD
REFUSE: values file: missing required key 'shasum'
exit=1
```

Injection — same values file, `L_shasum` exported:

```
$ L_shasum="$LAB/shasum_marker.sh" sh ./inst.sh \
      $LAB/packet.txt $LAB/vals_noshasum.txt HEAD
MARKER: env-supplied shasum executed with args: -a 256 …/lab/packet.txt
MARKER: env-supplied shasum executed with args: -a 256
REFUSE: packet line 1: unknown row type 'x'
exit=1
```

Two invocations of an environment-chosen program, both inside the pre-candidate
window, before the run stopped for an unrelated reason. The first is RA-02's
hash of the packet; the second is RA-03's re-hash of the snapshot.

### Why this matters more than the reachability suggests

`shasum` is not an incidental tool. It is the program whose output every
digest comparison in RA-02, RA-03, RA-07 and RA-08 is compared against:

* `:272-280` — the packet must equal `PACKET_SHA256`
* `:289-296` — the snapshot must equal the file
* `:528-532` — every closure blob must equal its reviewed digest
* `:538-541` — the artifact must equal `P_artifact_sha`

A hostile `shasum` does not need to know the expected values. It is handed the
packet's path in `argv` on its first call, so it can read the packet's `member`
rows and emit exactly the digest each later comparison wants. Every one of those
four comparisons then passes over bytes the launcher never actually checked, and
`exec /bin/sh "$T/$ARTIFACT_REL" stage1` (`:644-648`) hands control to whatever
was extracted. That is Rule 13's own named historical failure — "a replacement
`shasum` vouch for bytes it had just rewritten" — reproduced through the
environment instead of through `PATH`.

### Reachability, stated honestly

The precondition is a values file that omits one of the seven keys **and** an
exported `L_<key>`. Two counterweights belong in the record:

* The values file is already inside Cairn's accepted same-user residual
  (`bootstrap/reanchor-values.example:10-13` says so plainly). An adversary who
  can *write* that file can name `/tmp/evil-shasum` outright and needs none of
  this.
* An adversary who can only export a variable — a `.zshenv` line, a wrapper
  script, an earlier `export` in the operator's session — cannot exploit it
  against a *complete* values file; they get a `duplicate key` refusal.

So the class this enlarges is narrow: an operator whose values file is
incomplete gets an **ambient substitution where the design promised a loud
refusal**. But the launcher itself takes exactly this adversary seriously
elsewhere — `:607-612` refuses `/bin/zsh` precisely because zsh sources
`$HOME/.zshenv` non-interactively, "which puts the operator's own command
definitions straight back inside the supposedly clean child". The same dotfile
that defines a function can export a variable. The defence was applied to the
child and not to the parent.

Independently of exploitability, the property is **stated** in a security-rules
document and is false as stated, and this review chain (and the next one) reason
from that statement.

### Why the tests did not catch it

`bootstrap/tests/test_reanchor.py:1277-1284`,
`test_a_missing_field_refuses_with_no_ambient_fallback`, parametrises over all
seven launcher keys and asserts the refusal. It is a correct test of the channel
it models. The artifact-side sibling at `:428-439` is even better — it carries a
positive control (`"this node is vacuous unless PATH really could supply git"`).
Both build their environment as `dict(os.environ)`, which on any real machine
contains no `L_git` and no `V_python`. The pattern could not have matched. The
class is named `TestThereIsNoAmbientFallback` and covers `PATH` and `HOME`; the
variable-name channel was never modelled.

### The fix

One line at the top of `read_values`:

```
unset L_checkout L_git L_shasum L_mktemp L_mkdir L_cat L_env
```

That restores the property as written, keeps the duplicate check meaningful, and
changes no other behaviour. It changes the reviewed bytes, so it wants a fresh
instantiation and a fresh digest record — which is the mechanism working, not an
objection to the fix.

---

## L-2 — nothing binds the instance to the template

The header at `:3-9` states the model: the review "fills the ONE slot below with
the SHA-256 of the authorization packet it reviewed alongside these bytes, and
records the resulting launcher's own digest. The two travel together, out of
band, directly to the Maintainer." `bootstrap/REANCHOR_RUNBOOK.md:282-290`
repeats it and adds the operator's instruction: "Verify the digest of *that*
file against *that* record."

I looked for anything mechanical that enforces it and found nothing:

* not the authority closure (measured above — `False`);
* not the frozen gate surface (measured above — `False`);
* not `bootstrap/reanchor.sh` (`grep -c` → `0`);
* not the packet — `parse_packet` (`:303-416`) validates a `schema`,
  `provenance`, `artifact`, `artifact_sha256` and `member` rows, and refuses
  every other row type at `:372-373`. There is no launcher row and no place for
  one.

The two tests that read the template
(`bootstrap/tests/test_gate_preflight.py:4116-4142`) assert that
`EXPECTED_PATHS` equals `declared_authority_closure()` and is in `LC_ALL=C`
order. Both are checks on the *template's list*, in a suite the operator does
not run at ceremony time, against the repository copy — not against the file on
the Maintainer's disk.

**So the binding is exactly one act: a human comparing two hex strings, one from
a review document, one from `shasum` on the delivered file.** That act is
outside every check this repository owns. It is defensible — the whole point of
out-of-band delivery is that the candidate cannot touch it — but it must be
named, because the consequence is precise: *this review clears the text at
`9063e7d6…`, and clears nothing at all about the bytes the operator will run.*

Two smaller observations in the same area:

* The template refuses to run unfilled (`:266-269`, and my first control above
  shows it firing). Good: an unfilled template cannot be mistaken for an
  operative launcher.
* But the converse has no defence. A launcher with a *filled, well-formed* slot
  and altered logic passes every check in this tree, because there is no check.

---

## L-3 — a verifier that is not itself verified

The prior review's conclusion holds, and I reached it by different measurements
(above). What I want to add is the size of it, from the ceremony's own registry:

```
$ sh bootstrap/reanchor.sh steps
RA-01    pre-candidate launcher       …
RA-02    pre-candidate launcher       …
…
RA-09    pre-candidate launcher       …
RA-10    stage 1       stage1         THE FIRST CANDIDATE BYTE RUNS. …
```

Nine of nineteen steps, and specifically **every step that decides whether
candidate code starts**, are attributed by name to a component outside the
closure. `bootstrap/SAFETY.md:600-604` states the consequence itself: the
launcher "decides whether candidate code starts, so a substituted one is not
caught by anything downstream."

That is not a defect to fix inside this file — a launcher cannot verify itself
and there is no bootstrap that makes it possible. It is a property to state at
the top of the ceremony rather than in a rule two hundred lines into a safety
document, because it is the ceremony's single largest reliance on a human.

---

## L-4 — the `+10` delta from `d091cdd`

```
$ git diff $(git rev-parse refs/cairn/gate-anchor)..HEAD \
      -- bootstrap/reanchor-launcher.template.sh
@@ -630,6 +630,16 @@ if [ -n "$STAGE2_CONFIRM" ]; then
+CAIRN_LAUNCHER=$0
+CAIRN_PACKET=$PACKET_PATH
+CAIRN_CANDIDATE=$CANDIDATE_REF
+export CAIRN_LAUNCHER CAIRN_PACKET CAIRN_CANDIDATE
```

*(comment lines elided; the diff is a five-line comment and five lines of code.)*

**Does it touch the two-stage boundary? No, and I checked three ways.**

1. **Placement.** The hunk sits at `:633-641`, *after* the
   `if [ -n "$STAGE2_CONFIRM" ]` block closes at `:631`. Both stage-2 `exec`s
   (`:624-627`, `:629-630`) are upstream of it, so a stage-2 invocation never
   sets these variables. Stage 2 also runs no candidate code and prints no
   next-command block, so it has no use for them.
2. **Reach.** They are consumed at `bootstrap/reanchor.sh:543-547`, inside
   `cmd_stage1`, and only in `printf` arguments. The prior review grepped for
   this; I re-ran it and confirm `CAIRN_LAUNCHER`, `CAIRN_PACKET`,
   `CAIRN_CANDIDATE` appear in `reanchor.sh` at `:543-547` and nowhere else.
   (`bootstrap/PROVENANCE.md` uses the name `CAIRN_CANDIDATE` for an unrelated
   documented snippet; it is not this code path.)
3. **The key-bearing child.** The checker is invoked at
   `bootstrap/reanchor.sh:511-514` as
   `"$V_env" -i PATH=/usr/bin:/bin HOME="$V_home" "$V_python" -E -s "$CHECKER" "$@"`.
   `env -i` erases all three before the checker sees them.

**Stage 1 holds no key** (RA-12 probes the channel and refuses if it can sign)
and **stage 2 runs no candidate code** (L-5 below). The delta changes neither.

**It is a genuine fix, for the more dangerous half of prior finding R-1.** The
comment at `bootstrap/reanchor.sh:536-542` is accurate: an earlier version
printed `$0 stage2` and walked the operator around the launcher's re-extraction.
The delta is what lets stage 1 print the launcher command instead.

**One real defect in it.** `CAIRN_LAUNCHER=$0` is not canonicalised, and `$0` is
whatever the operator typed:

```
$ sh ./probe0.sh        →  dollar0=./probe0.sh
$ sh "$PWD/probe0.sh"   →  dollar0=/private/tmp/.../probe0.sh
```

`reanchor.sh:544` prints that string verbatim as a command to paste later, after
the operator has run `show-report`, `hash-package` and loaded the key. If the
launcher was invoked relatively, the printed command depends on the operator's
working directory at paste time. Usually that fails closed (no such file). It
does not fail closed if a *different* `reanchor-launcher.sh` sits in the
directory they happen to be in — and the entire trust model rests on running the
one whose digest they compared.

This file already owns the idiom for the fix: `:510` canonicalises `$T` with
`T=$(cd "$T" && pwd -P)`, with a comment explaining why an uncanonicalised path
broke a real ceremony. The same treatment for `$0`'s directory would close it.
Low severity, cheap fix, and it belongs to the delta rather than predating it.

`CAIRN_PACKET` is safe by construction — `PACKET_PATH` went through
`require_regular_file` (`:264`), so it is absolute and exists. `CANDIDATE_REF`
is unvalidated as a *string* (only as a resolvable rev), and is printed
unquoted; a rev-expression containing a space (`:/some message` resolves) would
print a command that splits into six arguments and hits the
`[ "$#" -eq 3 ]` refusal at `:440`. Fails closed. This is the prior review's S-3
seen from its source; the source is not worse than the sink.

---

## L-5 — the re-extraction property: where it holds, and where it does not

The prior review reported that `bootstrap/REANCHOR_RUNBOOK.md:172-174` claims
stage 2 "re-extracts and re-verifies its own bytes rather than reusing stage 1's"
while `:169` prints `sh bootstrap/reanchor.sh stage2 …`. I verified both halves
and can sharpen the consequence.

**The claim is false for the printed command, and the harm is concrete.**
`cmd_stage2` (`bootstrap/reanchor.sh:563-648`) parses values, calls
`require_checker`, validates the package, and execs the checker. It extracts
nothing and hashes no closure member. Worse, the checker it runs is resolved
from `$0`:

```
bootstrap/reanchor.sh:47-51
case $0 in
    */*) ARTIFACT_DIR=${0%/*} ;;
    *)   ARTIFACT_DIR=. ;;
esac
CHECKER=$ARTIFACT_DIR/tests/_gate_preflight.py
```

Run as `sh bootstrap/reanchor.sh stage2`, `ARTIFACT_DIR` is the **working tree's**
`bootstrap/`, so `CHECKER` is the working tree's `_gate_preflight.py`. Neither
that file nor the artifact itself is compared against any reviewed digest on
that path. So the runbook's printed command signs using an artifact **and** a
checker that candidate code — which ran, as the same user, in stage 1 — had a
window to rewrite, at the exact moment the key is loaded. That is not a
documentation slip; it is the printed instruction walking the operator into the
attack the two-stage split exists to prevent.

**The property does hold on the launcher's `--stage2` path, and I traced it.**
A `--stage2` invocation re-runs the entire pre-candidate sequence: `read_values`
(`:445`), `read_packet` (`:449`), `parse_packet` (`:450`), a fresh
`rev-parse` (`:484-486`), a **new** `mktemp -d` (`:491`), the per-blob digest
loop (`:519-535`), the artifact digest check (`:538-541`), and a freshly composed
manifest (`:548-557`) — then `exec /bin/sh "$T/$ARTIFACT_REL" stage2` at
`:624-630`. Because `ARTIFACT_DIR` derives from `$0`, the checker also resolves
inside `$T` — so both files come from the verified extraction, which is exactly
what `require_checker`'s comment at `bootstrap/reanchor.sh:373-378` claims
("Both arrive in one verified extraction").

**So the property holds somewhere. Two documents still point away from it.**

* `bootstrap/REANCHOR_RUNBOOK.md:166-174` — unchanged; still prints the direct
  command and still attributes the property to it. The prior review's R-1 is
  **not** closed by `d091cdd`.
* `bootstrap/reanchor.sh:809-812` — the `steps` registry itself puts RA-17 under
  `STAGE 2 / stage2` with the text "the confirmed package is validated against
  YOUR digest, re-extracted and re-verified". Read against the code, `stage2`
  does none of the re-extraction; the launcher does. A reader who trusts the
  registry — the runbook explicitly tells them to, at `:99-100` — will believe
  the direct command carries the property.

The fix for both is the same shape as the delta: name the launcher as the actor
for RA-17's re-extraction clause, and print the launcher's `--stage2` form in the
runbook.

---

## L-6 through L-9 — the shell-specific pass

I went looking for the usual hazards. Most are absent, and I want to record the
absences as well as the findings, because several of them are the result of
deliberate work visible in the comments.

**Clean.** No `eval` anywhere in the file (`grep` returns only prose backticks in
comments). No `PATH` reliance for any invoked program — every one goes through a
validated absolute path, and the git child runs under `env -i` with
`GIT_NO_LAZY_FETCH=1` set rather than inherited (`:472-479`, with a comment
explaining why absence is unsafe for that one variable). No word-splitting risk
I could find: `$T`, `$REL`, `$MANIFEST`, `"$@"` are quoted at every expansion
including the redirections at `:526` and `:557`. Both here-documents (`:375-377`,
`:402-404`, `:533-535`, `:583-585`) use an unquoted delimiter so `$PACKET_TEXT`
and `$P_rows` expand — the expansion is not recursive, so a packet containing
`$(…)` is inert. `parse_packet` blocks member-path traversal twice, at `:357-359`
(`/*|*..*|''`) and again by the fixed-set comparison at `:386-389`. The temporary
directory comes from `mktemp -d`, so it is not predictable and is mode 0700. The
control-character screen works — positive control:

```
$ printf 'checkout\t/x\n' > vals_tab.txt   # a tab is a control character
$ sh bootstrap/reanchor-launcher.template.sh $LAB/packet.txt $LAB/vals_tab.txt HEAD
REFUSE: values line 1 contains a control character
```

**L-6 — `--stage2 ''` silently runs stage 1.** `:436-439` sets
`STAGE2_CONFIRM=$5` with no shape check, and `:618` branches on `[ -n … ]`.
Replicating the branch exactly:

```
  five args, real digest:  -> STAGE 2 (confirm=deadbeef)
  five args, EMPTY digest: -> STAGE 1
```

By RA-16 the key is loaded before stage 2, and stage 1 refuses when the key can
sign — so this fails closed, loudly, with a diagnosis about the wrong stage.
`is_hex64 "$STAGE2_CONFIRM"` at the branch would make the message match the
mistake. The launcher already has that predicate at `:129-134`.

**L-7 — the closure-comparison guard is dead.** At `:577-578`:

```
ANCHORED=$(sterile_git cat-file blob "$ANCHOR_REF:$REL" 2>/dev/null \
           | "$L_SHASUM" -a 256) || ANCHORED=''
```

A pipeline's status is its last command's, and `shasum` succeeds on empty input:

```
$ A=$( (exit 9) | /usr/bin/shasum -a 256 ) || A='GUARD-FIRED'
$ printf 'A=%s\n' "$A"
A=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
```

`|| ANCHORED=''` never fires. The behaviour is nonetheless safe: a failed anchor
read yields the empty-input digest, which mismatches the reviewed row, so
`CLOSURE_CHANGED=yes` and the ceremony takes the transition path — the one that
*requires* a reviewed manifest. Failure biases toward the stricter mode, which is
the right direction. But the guard reads as protection it does not provide, and
this file's comments are load-bearing enough that a decorative one is a defect.

**L-8 — `MAX_PACKET_BYTES` is declared at `:39` and never used.**
`MAX_VALUES_BYTES` and `MAX_LINE_BYTES` are both enforced (`:161-164`,
`:318-319`); the packet gets a per-line bound and no whole-file bound, so
`PACKET_TEXT` is unbounded at `:285`. In practice the digest binding at
`:277-280` means only a packet the review actually produced can get that far, so
the exposure is a memory-size question and not an authority question. Remove it
or enforce it; leaving it declared implies a check that is not there.

**L-9 — no `trap`, and `$T` outlives the run.** `:614-617` documents that `exec`
means `$T` is not cleaned up, which is correct and unavoidable. Not documented:
every `die` after `:491` also leaves `$T` behind, as does any signal. Nothing
later reuses a `$T` (each run makes a new one), so this is hygiene, not a
vulnerability — but stage 1's `$T` contains an extracted copy of the whole
authority closure and persists indefinitely under the system temp directory.
Worth a line in the runbook's cleanup step.

---

## L-10 — out of scope, but I will not leave it unsaid

The same environment-injection defect exists in `bootstrap/reanchor.sh`, a file
the prior review admitted. `:247-259` uses the identical `${V_x+s}` idiom under
a comment (`:243-246`) that repeats the strongest version of the claim: "It is
never filled from PATH, HOME, Git config or any other ambient source."

Control — values file with `python` removed, clean environment:

```
$ sh bootstrap/reanchor.sh validate $LAB/v2_nopython.txt
REFUSE: missing required key 'python'
```

Same file, one exported variable:

```
$ V_python=/Users/kendal30/conda_envs/lhm/bin/python3.13 \
      sh bootstrap/reanchor.sh validate $LAB/v2_nopython.txt
  …
  OK: the values file satisfies the closed schema.
```

Two things make this worse than the launcher's version:

1. `V_python` is the interpreter that runs the checker
   (`bootstrap/reanchor.sh:511-514`, `:643-647`) — the program that decides
   whether the anchor moves.
2. `print_effective_configuration` prints the injected value under a header that
   reads `(read from $1 -- nothing below was discovered)`
   (`bootstrap/reanchor.sh:319-321`). The stop-point the contract relies on —
   RA-11, "the complete effective configuration is shown while it is still free
   to stop" — displays an ambient value as though it came from the file, and
   states in the same breath that nothing was discovered.

The launcher `exec`s the artifact with its own inherited environment
(`:644-648`), so it is the conduit for this as well as having its own copy. I am
flagging rather than reviewing: `bootstrap/reanchor.sh` is a closure member, it
is not my scope, and a change there needs its own admission.

---

## Does the RA-01 … RA-09 property hold?

**Conditionally, and the conditions are not all inside the ceremony.**

| step | what it needs | holds? |
|---|---|---|
| RA-01 | the values file parses; every executable is *recorded* | **logic yes, property NO** — L-1: an omitted key is filled from the environment |
| RA-02 | packet on disk equals the digest bound into the launcher | yes, **conditional on `shasum`** (L-1) |
| RA-03 | bytes hashed equal bytes parsed | yes, **conditional on `shasum`** (L-1) |
| RA-04 | packet's member set equals the launcher's fixed list | **yes, unconditionally** — shell string equality at `:386`, no external utility |
| RA-05 | artifact is a closure member: one row, matching digest, expected path | **yes, unconditionally** — `:394-415`, shell-internal |
| RA-06 | candidate resolved once to a full OID | yes; `--end-of-options` and a hex screen at `:484-489` |
| RA-07 | every closure blob at that OID matches its reviewed digest | yes, **conditional on `shasum`** (L-1) |
| RA-08 | extracted artifact matches its reviewed digest | yes, **conditional on `shasum`** (L-1) |
| RA-09 | manifest composed from packet + resolution, nothing from the candidate | **yes, unconditionally** — I traced every value at `:548-557` to `REVIEW_MANIFEST_SCHEMA`, `$RESOLVED`, `$P_provenance`, `$P_rows`; none is read from `$T` |

And over all nine, one condition that is not in the table because it is not in
the file: **the operator must be running the launcher the review produced**, and
nothing checks that (L-2, L-3).

RA-04, RA-05, RA-09 and the structural half of RA-06 hold on their own merits —
they are done with shell builtins, which is why the file keeps saying "no utility
joins the pre-candidate trust set for this check" (`:51-52`, `:273-274`,
`:508-509`). That discipline is real and it is what makes those four
unconditional. The five that need a digest are the five L-1 reaches.

---

## What an operator running this launcher is actually relying on, and what they are not

**They are relying on:**

* **Their own eyes, once, on a hex string.** That there is no mechanical check on
  the launcher's identity is the single largest reliance in the ceremony, and it
  is invisible at the moment it matters — the operator types one command and the
  launcher prints a confident banner (`:587-599`).
* **Their values file naming all seven executables.** Not for the reason the
  documents give (that absence refuses), but because a *complete* file is what
  makes the environment channel fail closed. An incomplete one substitutes
  silently.
* **Their shell's environment containing no `L_*` or `V_*` variable.** Nothing
  states this, nothing checks it, and no test models it.
* **The reviewed packet and the launcher having travelled together and neither
  having been altered in transit.** The launcher checks the packet against
  itself; nothing checks the launcher.
* **Reading the launcher's printed next-command rather than the runbook's**, for
  stage 2. The two disagree (L-5), and the printed one became correct only in
  `d091cdd`.

**They are not relying on** — these hold independently of the operator:

* the closure member *set* being the reviewed one (RA-04) — a shell comparison
  against bytes inside the launcher, no utility involved;
* the artifact being a closure member rather than a file named alongside it
  (RA-05);
* the review manifest containing nothing the candidate wrote (RA-09) — I traced
  it;
* the candidate being read at one immutable OID rather than a ref that can move
  under them (RA-06);
* the git child being free of ambient `GIT_*` steering and of promisor-triggered
  transport helpers (`:455-471`) — the reasoning there is the best in the file
  and it is backed by a reproduced attack;
* transition-versus-steady-state being **measured** rather than chosen
  (`:559-585`), which removes the operator's ability to declare "steady state"
  over a real closure change;
* stage 2, when launched through `--stage2`, running an artifact and a checker
  that both come from a fresh verified extraction (L-5).

**What they are relying on but should not have to:** that the two `printf`
blocks at `bootstrap/reanchor.sh:543-556` are the authority on how to run stage
2, rather than the runbook and the `steps` registry that both still point at the
unverified path.

---

## What I could not reach

* **The ceremony.** I did not run `stage1` or `stage2`, did not touch
  `refs/cairn/*`, and did not go near a key. So every claim about what happens
  *after* `exec` is read from the code, not observed. Specifically: I traced but
  did not execute the launcher's `--stage2` re-extraction, and my statement that
  it delivers the property rests on reading `:436-439`, `:445-450`, `:491`,
  `:519-541` and `:618-631` against `bootstrap/reanchor.sh:47-51` and `:373-383`.
* **The instantiated launcher.** It does not exist in this tree and, by design,
  never will. Everything I admit is about `9063e7d6…`; the operative file is
  produced by the review that fills the slot, and I did not produce one for
  delivery. My scratchpad instantiation was a probe, is not an operative
  launcher, and should not be treated as one.
* **A hostile-`shasum` end-to-end demonstration.** I proved the injected program
  executes twice in the pre-candidate window. I did not build a `shasum` that
  forges all four comparisons and let the launcher `exec` a mismatched artifact,
  because that means running the ceremony's handoff. The step from "the
  environment chooses the digest tool" to "the digest tool can forge the
  comparisons" is an argument, not a measurement — though I consider it a short
  one, since the packet's path is in the tool's own `argv`.
* **The full test suite.** This is a review of one file against the reviewed
  bytes, not an integration boundary. I ran targeted probes only, all read-only,
  all in a scratchpad. I did not run `CAIRN_FULL_SUITE=1 python -m pytest
  bootstrap/tests`.
* **`bootstrap/reanchor.sh`, `bootstrap/REANCHOR_RUNBOOK.md`, and
  `bootstrap/SAFETY.md`.** All three make claims I found to be false or
  overstated (L-1, L-5, L-10), and all three are outside my scope. I did not
  review them; I read exactly the passages needed to test the launcher's
  contract, and I have not checked whether they contain other defects of the same
  kind.
* **Independence.** Cairn's External floor is "a different agent type, or a
  human." Like the review before it, this one is a same-agent fresh session and
  shares that session's model and priors. I compensated the only way available:
  every finding above has a command and an output, every absence has a positive
  control, and I re-derived the prior review's two framing facts rather than
  accepting them. That is not the same as structural independence, and the
  Maintainer should weight it accordingly.
