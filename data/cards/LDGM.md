## LDGM
_ARM A64 Instruction_

**Title**: LDGM -- A64 | **Class**: `general` | **XML ID**: `LDGM`

**Architecture**: `FEAT_MTE2` (ARMv8.5)

**Summary**: Load tag multiple

**Description**:
This instruction reads a naturally aligned block of N Allocation Tags,
where the size of N is identified in GMID_EL1.BS, and writes the Allocation Tag read from address A to the destination register at
4*A<7:4>+3:4*A<7:4>. Bits of the destination register not written with an
Allocation Tag are set to 0.

This instruction is UNDEFINED at EL0.

This instruction generates an Unchecked access.

### Variant: `Integer`
- **Assembly**: `LDGM  <Xt>, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24 23  21 20  11   9   4  |
|-----------------------------------|
| 1101 1   0   0   1   11  1   000000000 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldsttags.LDGM_64bulk_ldsttags)

```
if !IsFeatureImplemented(FEAT_MTE2) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
```

#### Execute (A64.ldst.ldsttags.LDGM_64bulk_ldsttags)

```
if PSTATE.EL == EL0 then UNDEFINED;

bits(64) data = Zeros(64);
bits(64) address;

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant integer size = 4 * (2 ^ (UInt(GMID_EL1.BS)));
address = Align(address, size);
constant integer count = size >> LOG2_TAG_GRANULE;
integer index = UInt(address<LOG2_TAG_GRANULE+3:LOG2_TAG_GRANULE>);
constant boolean stzgm = FALSE;
constant AccessDescriptor accdesc = CreateAccDescLDGSTG(MemOp_LOAD, stzgm);

for i = 0 to count-1
    constant bits(4) tag = AArch64.MemTag[address, accdesc];
    Elem[data, index, 4] = tag;
    address = AddressIncrement(address, TAG_GRANULE, accdesc);
    index = index + 1;

X[t, 64] = data;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldgm.xml`
</details>