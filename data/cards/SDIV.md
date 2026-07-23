## SDIV
_ARM A64 Instruction_

**Title**: SDIV -- A64 | **Class**: `general` | **XML ID**: `SDIV`

**Summary**: Signed divide

**Description**:
This instruction divides the first signed source register value
by the second signed source register value, and writes the result
to the destination register. Dividing by zero writes the value zero to the destination register.
The condition flags are not affected.

### Variant: `Integer (SDIV_32_dp_2src)` (32-bit)
- **Condition**: `sf == 0`
- **Assembly**: `SDIV  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  10  9   4  |
|-----------------------------|
| sf  0   0   11010110 Rm  00001 1   Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.SDIV_32_dp_2src)

```
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 32 << UInt(sf);
```

#### Execute (A64.dpreg.dp_2src.SDIV_32_dp_2src)

```
constant bits(datasize) operand1 = X[n, datasize];
constant bits(datasize) operand2 = X[m, datasize];
constant integer dividend = SInt(operand1);
constant integer divisor  = SInt(operand2);
integer result;
if divisor == 0 then
    result = 0;
elsif (dividend < 0) == (divisor < 0) then
    result = Abs(dividend) DIV Abs(divisor);    // same signs - positive result
else
    result = -(Abs(dividend) DIV Abs(divisor)); // different signs - negative result
X[d, datasize] = result<datasize-1:0>;
```

### Variant: `Integer (SDIV_64_dp_2src)` (64-bit)
- **Condition**: `sf == 1`
- **Assembly**: `SDIV  <Xd>, <Xn>, <Xm>`
- **Fixed bits**: `sf`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  10  9   4  |
|-----------------------------|
| sf  0   0   11010110 Rm  00001 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sdiv.xml`
</details>