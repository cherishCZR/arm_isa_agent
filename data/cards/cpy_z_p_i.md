## CPY
_ARM A64 Instruction_

**Title**: CPY (immediate, merging) -- A64 | **Class**: `sve` | **XML ID**: `cpy_z_p_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Copy signed integer immediate to vector elements (merging)

**Description**:
Copy a signed integer immediate
to each active element in the destination vector.
Inactive elements in the destination vector register remain unmodified.

The immediate operand is a signed value in the range -128 to
+127, and for element widths of 16 bits or higher it may also be
a signed multiple of 256 in the range -32768 to +32512 (excluding 0).

The immediate is encoded in 8 bits with an optional left shift
by 8. The preferred disassembly when the shift option is
specified is "#<simm8>, LSL #8".
However an assembler and
disassembler may also allow use of the shifted 16-bit value unless the
immediate is 0 and the shift amount is 8, which must be
unambiguously described as "#0, LSL #8".

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `CPY  <Zd>.<T>, <Pg>/M, #<imm>{, <shift>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  15 14 13 12   4  |
|-----------------------------------|
| 000 0010 1   size 01  Pg  0   1   sh  imm8 Zd  |
```

#### Decode (A64.sve.sve_wideimm_pred.sve_int_dup_imm_pred.cpy_z_p_i_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size:sh == '001' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
integer imm = SInt(imm8);
if sh == '1' then imm = imm << 8;
```

#### Execute (A64.sve.sve_wideimm_pred.sve_int_dup_imm_pred.cpy_z_p_i_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) dest = if merging then Z[d, VL] else Zeros(VL);
bits(VL) result;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, esize] = imm<esize-1:0>;
    else
        Elem[result, e, esize] = Elem[dest, e, esize];

Z[d, VL] = result;
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
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<imm>` | `immediate` | `imm8` | Is a signed immediate in the range -128 to 127, encoded in the "imm8" field. |
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
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instructio
... (truncated)

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cpy_z_p_i.xml`
</details>