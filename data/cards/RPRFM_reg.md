## RPRFM
_ARM A64 Instruction_

**Title**: RPRFM -- A64 | **Class**: `general` | **XML ID**: `RPRFM_reg`

**Architecture**: `FEAT_RPRFM` (ARMv8.9)

**Summary**: Range prefetch memory

**Description**:
This instruction signals the memory system that
data memory accesses from a specified range of addresses are likely to occur
in the near future. The instruction may also signal the memory system about
the likelihood of data reuse of the specified range of addresses.
The memory system can respond by taking actions that are
expected to speed up the memory accesses when they do occur,
such as prefetching locations within the specified address ranges
into one or more caches. The memory system may also exploit the data reuse
hints to decide whether to retain the data in other caches upon eviction
from the innermost caches or to discard it.

The effect of an RPRFM instruction is IMPLEMENTATION DEFINED.
For more information, see Prefetch memory.

An RPRFM instruction specifies the type of accesses and range of addresses using
the following parameters:

### Variant: `Integer`
- **Assembly**: `RPRFM  (<rprfop>|#<imm6>), <Xm>, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  15  12 11   9   4  |
|--------------------------------------------|
| 11  11  1   0   0   0   10  1   Rm  x1x S   10  Rn  11xxx |
```

#### Decode (A64.ldst.ldst_regoff.RPRFM_R_ldst_regoff)

```
if !IsFeatureImplemented(FEAT_RPRFM) then EndOfDecode(Decode_NOP);
constant bits(6) operation = option<2>:option<0>:S:Rt<2:0>;
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.ldst.ldst_regoff.RPRFM_R_ldst_regoff)

```
constant bits(64) address  = if n == 31 then SP[64] else X[n, 64];
constant bits(64) metadata = X[m, 64];
constant integer stride = SInt(metadata<59:38>);
constant integer count  = UInt(metadata<37:22>) + 1;
constant integer length = SInt(metadata<21:0>);
integer reuse;

if metadata<63:60> == '0000' then
    reuse = -1; // Not known
else
    reuse = 32768 << (15 - UInt(metadata<63:60>));

Hint_RangePrefetch(address, length, stride, count, reuse, operation);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_RPRFM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<rprfop>` | `unknown` | `option:S:Rt` | Is the range prefetch operation, defined as <type><policy>.           <type> is one of:                                       PLD               Prefet |
| `<imm6>` | `immediate` | `option:S:Rt` | Is the range prefetch operation encoding as an immediate, in the range 0 to 63, encoded in "option<2>:option<0>:S:Rt<2:0>". This syntax is only for en |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose register that holds an encoding of the metadata, encoded in the "Rm" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

**<rprfop> Value Table**:

| bitfield | symbol |
|---|---|
| 11000 | PLDKEEP |
| 11001 | PSTKEEP |
| 11100 | PLDSTRM |
| 11101 | PSTSTRM |

---
<details><summary>Metadata</summary>

- isa: `A64`
- offset-type: `off-reg`
- source: `rprfm_reg.xml`
</details>