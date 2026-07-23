## UBFM
_ARM A64 Instruction_

**Title**: UBFM -- A64 | **Class**: `general` | **XML ID**: `UBFM`

**Summary**: Unsigned bitfield move

**Description**:
This instruction is usually accessed via one of its aliases,
which are always preferred for disassembly.

If <imms> is greater than or equal to <immr>,
this copies a bitfield of (<imms>-<immr>+1) bits
starting from bit position <immr> in the source register
to the least significant bits of the destination register.

If <imms> is less than <immr>, this copies a
bitfield of (<imms>+1) bits from the least significant
bits of the source register to bit position
(regsize-<immr>) of the destination register, where
regsize is the destination register size of 32 or 64 bits.

In both cases, the destination bits below and above the bitfield are
set to zero.

### Variant: `With zeros to left and right (UBFM_32M_bitfield)` (32-bit)
- **Condition**: `sf == 0 && N == 0`
- **Assembly**: `UBFM  <Wd>, <Wn>, #<immr>, #<imms>`
- **Fixed bits**: `sf`=`0`, `N`=`0`
- **Bit Pattern**: `??????????????????????0????????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  10  100110 N   immr imms Rn  Rd  |
```

#### Decode (A64.dpimm.bitfield.UBFM_32M_bitfield)

```
if sf == '1' && N != '1' then EndOfDecode(Decode_UNDEF);
if sf == '0' && (N != '0' || immr<5> != '0' || imms<5> != '0') then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sf);
constant integer s = UInt(imms);
constant integer r = UInt(immr);

bits(datasize) wmask;
bits(datasize) tmask;
(wmask, tmask) = DecodeBitMasks(N, imms, immr, FALSE, datasize);
```

#### Execute (A64.dpimm.bitfield.UBFM_32M_bitfield)

```
constant bits(datasize) src = X[n, datasize];

// Perform bitfield move on low bits
constant bits(datasize) bot = ROR(src, r) AND wmask;

// Combine extension bits and result bits
X[d, datasize] = bot AND tmask;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `sf != '1' \|\| N == '1'` |
| 🚫 ENCODING_UNDEF | `sf != '0' \|\| (N == '0' && immr<5> == '0' && imms<5> == '0')` |

### Variant: `With zeros to left and right (UBFM_64M_bitfield)` (64-bit)
- **Condition**: `sf == 1 && N == 1`
- **Assembly**: `UBFM  <Xd>, <Xn>, #<immr>, #<imms>`
- **Fixed bits**: `sf`=`1`, `N`=`1`
- **Bit Pattern**: `??????????????????????1????????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  22 21  15   9   4  |
|--------------------------|
| sf  10  100110 N   immr imms Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Wn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the general-purpose source register, encoded in the "Rn" field. |
| `<immr>` | `immediate` | `immr` | For the "32-bit" variant: is the right rotate amount, in the range 0 to 31, encoded in the "immr" field. |
| `<immr>` | `immediate` | `immr` | For the "64-bit" variant: is the right rotate amount, in the range 0 to 63, encoded in the "immr" field. |
| `<imms>` | `immediate` | `imms` | For the "32-bit" variant: is the leftmost bit number to be moved from the source, in the range 0 to 31, encoded in the "imms" field. |
| `<imms>` | `immediate` | `imms` | For the "64-bit" variant: is the leftmost bit number to be moved from the source, in the range 0 to 63, encoded in the "imms" field. |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

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

- bitfield-fill: `zero-fill`
- isa: `A64`
- source: `ubfm.xml`
</details>