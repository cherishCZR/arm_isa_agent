## LDAP1
_ARM A64 Instruction_

**Title**: LDAP1 (SIMD&FP) -- A64 | **Class**: `advsimd` | **XML ID**: `LDAP1_advsimd_sngl`

**Architecture**: `FEAT_AdvSIMD && FEAT_LRCPC3` (FEAT_AdvSIMD && FEAT_LRCPC3)

**Summary**: Load-acquire RCpc one single-element structure to one lane of one register

**Description**:
This instruction loads a single-element structure from memory and writes the result to the specified lane of the SIMD&FP
register without affecting the other bits of the register.

The instruction has memory ordering semantics, as described in
Load-Acquire, Load-AcquirePC, and Store-Release, except that:

This difference in memory ordering is not described in the pseudocode.

For information about addressing modes, see Load/Store addressing modes.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `64-bit`
- **Assembly**: `LDAP1  { <Vt>.D }[<index>], [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  27 26 25 24  22 21 20  16 15  12 11   9   4  |
|--------------------------------------------------|
| 0   Q   00  1   1   0   10  1   0   0000 1   100 0   01  Rn  Rt  |
```

#### Decode (A64.ldst.asisdlso.LDAP1_asisdlso_D1)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_LRCPC3) then
    EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = integer UNKNOWN;
constant boolean wback = FALSE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Postdecode (A64.ldst.asisdlso.LDAP1_asisdlso_D1)

```
bits(2) scale = opcode<2:1>;
constant integer selem = UInt(opcode<0>:R) + 1;
boolean replicate = FALSE;
integer index;

case scale of
    when '11'
        // load and replicate
        if L == '0' || S == '1' then EndOfDecode(Decode_UNDEF);
        scale = size;
        replicate = TRUE;
    when '00'
        index = UInt(Q:S:size);       // B[0-15]
    when '01'
        if size<0> == '1' then EndOfDecode(Decode_UNDEF);
        index = UInt(Q:S:size<1>);    // H[0-7]
    when '10'
        if size<1> == '1' then EndOfDecode(Decode_UNDEF);
        if size<0> == '0' then
            index = UInt(Q:S);        // S[0-3]
        else
            if S == '1' then EndOfDecode(Decode_UNDEF);
            index = UInt(Q);          // D[0-1]
            scale = '11';

constant integer datasize = 64 << UInt(Q);
constant integer esize = 8 << UInt(scale);
```

#### Execute (A64.ldst.asisdlso.LDAP1_asisdlso_D1)

```
CheckFPAdvSIMDEnabled64();

bits(64) address;
bits(64) eaddr;
bits(64) offs;
bits(128) rval;
bits(esize) element;
constant integer ebytes = esize DIV 8;

constant AccessDescriptor accdesc = CreateAccDescASIMDAcqRel(MemOp_LOAD, tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

offs = Zeros(64);

if replicate then
    // load and replicate to all elements
    for s = 0 to selem-1
        eaddr = AddressIncrement(address, offs, accdesc);
        element = Mem[eaddr, ebytes, accdesc];
        // replicate to fill 128- or 64-bit register
        V[t, datasize] = Replicate(element, datasize DIV esize);
        offs = offs + ebytes;
        t = (t + 1) MOD 32;
else
    // load/store one element per register
    for s = 0 to selem-1
        rval = V[t, 128];
        eaddr = AddressIncrement(address, offs, accdesc);
        Elem[rval, index, esize] = Mem[eaddr, ebytes, accdesc];
        V[t, 128] = rval;
        offs = offs + ebytes;
        t = ( t + 1 ) MOD 32;
if wback then
    if m != 31 then
        offs = X[m, 64];
    address = AddressAdd(address, offs, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

#### Constraints
_4× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_LRCPC3)` |
| 🚫 ENCODING_UNDEF | `L != '0' && S != '1'` |
| 🚫 ENCODING_UNDEF | `size<0> != '1'` |
| 🚫 ENCODING_UNDEF | `size<1> != '1'` |
| 🚫 ENCODING_UNDEF | `S != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vt>` | `register (128-bit)` | `Rt` | Is the name of the first or only SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<index>` | `unknown` | `Q` | Is the element index, encoded in "Q". |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- as-structure-org: `of-doublewords`
- as-structure-post-index: `as-no-post-index`
- isa: `A64`
- source: `ldap1_advsimd_sngl.xml`
</details>