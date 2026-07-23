## CRC32C
_ARM A64 Instruction_

**Title**: CRC32CB, CRC32CH, CRC32CW, CRC32CX -- A64 | **Class**: `general` | **XML ID**: `CRC32C`

**Architecture**: `FEAT_CRC32` (ARMv8.0)

**Summary**: CRC32C checksum

**Description**:
This instruction performs a cyclic redundancy check (CRC)
calculation on a value held in a general-purpose register. It takes
an input CRC value in the first source operand, performs a CRC on
the input value in the second source operand, and returns the output
CRC value. The second source operand can be 8, 16, 32, or 64
bits. To align with common usage, the bit order of the values is
reversed as part of the operation, and the polynomial
0x1EDC6F41 is used for the CRC calculation.

In an Armv8.0 implementation, this is an OPTIONAL instruction.
From Armv8.1, it is mandatory for all implementations to implement this instruction.

### Variant: `CRC (CRC32CB_32C_dp_2src)` (CRC32CB)
- **Condition**: `sf == 0 && sz == 00`
- **Assembly**: `CRC32CB  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`, `sz`=`00`
- **Bit Pattern**: `??????????00???????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  12 11   9   4  |
|--------------------------------|
| sf  0   0   11010110 Rm  010 1   sz  Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.CRC32CB_32C_dp_2src)

```
if !IsFeatureImplemented(FEAT_CRC32) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
if sf == '1' && sz != '11' then EndOfDecode(Decode_UNDEF);
if sf == '0' && sz == '11' then EndOfDecode(Decode_UNDEF);
constant integer size = 8 << UInt(sz);
```

#### Execute (A64.dpreg.dp_2src.CRC32CB_32C_dp_2src)

```
constant bits(32)      acc     = X[n, 32];     // accumulator
constant bits(size)    val     = X[m, size];   // input value
constant bits(32)      poly    = 0x1EDC6F41<31:0>;

constant bits(32+size) tempacc = BitReverse(acc):Zeros(size);
constant bits(size+32) tempval = BitReverse(val):Zeros(32);

// Poly32Mod2 on a bitstring does a polynomial Modulus over {0,1} operation
X[d, 32] = BitReverse(Poly32Mod2(tempacc EOR tempval, poly));
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CRC32)` |
| 🚫 ENCODING_UNDEF | `sf != '1' \|\| sz == '11'` |
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| sz != '11'` |

### Variant: `CRC (CRC32CH_32C_dp_2src)` (CRC32CH)
- **Condition**: `sf == 0 && sz == 01`
- **Assembly**: `CRC32CH  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`, `sz`=`01`
- **Bit Pattern**: `??????????10???????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  12 11   9   4  |
|--------------------------------|
| sf  0   0   11010110 Rm  010 1   sz  Rn  Rd  |
```

### Variant: `CRC (CRC32CW_32C_dp_2src)` (CRC32CW)
- **Condition**: `sf == 0 && sz == 10`
- **Assembly**: `CRC32CW  <Wd>, <Wn>, <Wm>`
- **Fixed bits**: `sf`=`0`, `sz`=`10`
- **Bit Pattern**: `??????????01???????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  12 11   9   4  |
|--------------------------------|
| sf  0   0   11010110 Rm  010 1   sz  Rn  Rd  |
```

### Variant: `CRC (CRC32CX_64C_dp_2src)` (CRC32CX)
- **Condition**: `sf == 1 && sz == 11`
- **Assembly**: `CRC32CX  <Wd>, <Wn>, <Xm>`
- **Fixed bits**: `sf`=`1`, `sz`=`11`
- **Bit Pattern**: `??????????11???????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  12 11   9   4  |
|--------------------------------|
| sf  0   0   11010110 Rm  010 1   sz  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose accumulator output register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose accumulator input register, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the general-purpose data source register, encoded in the "Rm" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose data source register, encoded in the "Rm" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- feature: `crc`
- isa: `A64`
- source: `crc32c.xml`
</details>