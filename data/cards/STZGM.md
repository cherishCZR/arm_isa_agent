## STZGM
_ARM A64 Instruction_

**Title**: STZGM -- A64 | **Class**: `general` | **XML ID**: `STZGM`

**Architecture**: `FEAT_MTE2` (ARMv8.5)

**Summary**: Store Allocation Tag and zero multiple

**Description**:
This instruction writes a naturally aligned block of N Allocation Tags
and stores zero to the associated data locations, where the size of N
is identified in DCZID_EL0.BS, and the Allocation Tag
is taken from the source register bits<3:0>.

This instruction is UNDEFINED at EL0.

This instruction generates an Unchecked access.

### Variant: `Integer`
- **Assembly**: `STZGM  <Xt>, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24 23  21 20  11   9   4  |
|-----------------------------------|
| 1101 1   0   0   1   00  1   000000000 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldsttags.STZGM_64bulk_ldsttags)

```
if !IsFeatureImplemented(FEAT_MTE2) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
```

#### Execute (A64.ldst.ldsttags.STZGM_64bulk_ldsttags)

```
if PSTATE.EL == EL0 then UNDEFINED;

constant bits(64) data = X[t, 64];
constant bits(4) tag = data<3:0>;
bits(64) address;
if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant integer size = 4 * (2 ^ (UInt(DCZID_EL0.BS)));
address = Align(address, size);
constant integer count = size >> LOG2_TAG_GRANULE;
constant boolean stzgm = TRUE;
constant AccessDescriptor accdesc = CreateAccDescLDGSTG(MemOp_STORE, stzgm);

for i = 0 to count-1
    AArch64.MemTag[address, accdesc] = tag;
    Mem[address, TAG_GRANULE, accdesc] = Zeros(8*TAG_GRANULE);
    address = AddressIncrement(address, TAG_GRANULE, accdesc);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `stzgm.xml`
</details>