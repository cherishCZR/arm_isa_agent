## SUB
_ARM A64 Instruction_

**Title**: SUB (immediate) -- A64 | **Class**: `sve` | **XML ID**: `sub_z_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Subtract immediate (unpredicated)

**Description**:
Subtract an unsigned immediate from
each element of the source vector,
and destructively place the results in the corresponding elements of the  source vector. This instruction is unpredicated.

The immediate is an unsigned value in the range 0 to 255, and
for element widths of 16 bits or higher it may also be a
positive multiple of 256 in the range 256 to 65280.

The immediate is encoded in 8 bits with an optional left shift
by 8. The preferred disassembly when the shift option is
specified is "#<uimm8>, LSL #8".
However an assembler and
disassembler may also allow use of the shifted 16-bit value unless the
immediate is 0 and the shift amount is 8, which must be
unambiguously described as "#0, LSL #8".

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `SUB  <Zdn>.<T>, <Zdn>.<T>, #<imm>{, <shift>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  13 12   4  |
|-----------------------------------|
| 001 0010 1   size 1   00  001 11  sh  imm8 Zdn |
```

#### Decode (A64.sve.sve_wideimm_unpred.sve_int_arith_imm0.sub_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size:sh == '001' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn);
integer imm = UInt(imm8);
if sh == '1' then imm = imm << 8;
```

#### Execute (A64.sve.sve_wideimm_unpred.sve_int_arith_imm0.sub_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[dn, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    Elem[result, e, esize] = element1 - imm;

Z[dn, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size:sh != '001'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<imm>` | `immediate` | `imm8` | Is an unsigned immediate in the range 0 to 255, encoded in the "imm8" field. |
| `<shift>` | `shift` | `sh` | Is the optional left shift to apply to the immediate, defaulting to LSL #0 and |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | LSL #0 |
| 1 | LSL #8 |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sub_z_zi.xml`
</details>