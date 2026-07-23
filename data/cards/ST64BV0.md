## ST64BV0
_ARM A64 Instruction_

**Title**: ST64BV0 -- A64 | **Class**: `general` | **XML ID**: `ST64BV0`

**Architecture**: `FEAT_LS64_ACCDATA` (ARMv8.7)

**Summary**: Single-copy atomic 64-byte EL0 store with status result

**Description**:
This instruction stores eight 64-bit doublewords from
consecutive registers to a memory location, with the bottom 32 bits taken from
ACCDATA_EL1, and writes the status result of the store to a register.
The store starts at register Xt, with the data being formed as Data<511:0>
 = X(t+7):X(t+6):X(t+5):X(t+4):X(t+3):X(t+2):X(t+1):Xt<63:32>:ACCDATA_EL1<31:0>.
The data is stored atomically and is required to be 64-byte aligned.

It is IMPLEMENTATION DEFINED which memory locations support this instruction.
A memory location that supports ST64BV0 also supports
ST64BV.
For more information, including about the memory types accessible and how the accesses are
performed, see Single-copy atomic 64-byte load/store.

### Variant: `Integer`
- **Assembly**: `ST64BV0  <Xs>, <Xt>, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23 22 21 20  15 14  11   9   4  |
|-----------------------------------------------|
| 11  11  1   0   0   0   0   0   1   Rs  1   010 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.ST64BV0_64_memop)

```
if !IsFeatureImplemented(FEAT_LS64_ACCDATA) then EndOfDecode(Decode_UNDEF);
if Rt<4:3> == '11' || Rt<0> == '1' then EndOfDecode(Decode_UNDEF);
constant boolean withstatus = TRUE;
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.ST64BV0_64_memop)

```
CheckST64BV0Enabled();

bits(512) data;
bits(64) address;
bits(64) value;

constant AccessDescriptor accdesc = CreateAccDescLS64(MemOp_STORE, withstatus, tagchecked);

constant bits(64) Xt = X[t, 64];
value<31:0> = ACCDATA_EL1<31:0>;
value<63:32> = Xt<63:32>;
if BigEndian(accdesc.acctype) then value = BigEndianReverse(value);
data<63:0> = value;

for i = 1 to 7
    value = X[t+i, 64];
    if BigEndian(accdesc.acctype) then value = BigEndianReverse(value);
    data<63+64*i : 64*i> = value;

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(64) status = MemStore64BWithRet(address, data, accdesc);

if s != 31 then X[s, 64] = status;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LS64_ACCDATA)` |
| 🚫 ENCODING_UNDEF | `Rt<4:3> != '11' && Rt<0> != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register into which the status result of this instruction is written, encoded in the "Rs" field. The value r |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `st64bv0.xml`
</details>