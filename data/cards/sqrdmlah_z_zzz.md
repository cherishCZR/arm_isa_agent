## SQRDMLAH
_ARM A64 Instruction_

**Title**: SQRDMLAH (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `sqrdmlah_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating rounding doubling multiply-add high to accumulator (unpredicated)

**Description**:
Multiply then double the corresponding signed elements of the
first and second source vectors, and destructively add the
rounded high half of each result to the corresponding elements
of the addend and destination vector.
Each destination element is saturated to the
 N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `SQRDMLAH  <Zda>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14  10  9   4  |
|-----------------------------------|
| 010 0010 0   size 0   Zm  0   1110 0   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_muladd_unpred.sve_intx_qrdmlah.sqrdmlah_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_intx_muladd_unpred.sve_intx_qrdmlah.sqrdmlah_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = SInt(Elem[operand1, e, esize]);
    constant integer element2 = SInt(Elem[operand2, e, esize]);
    constant integer element3 = SInt(Elem[operand3, e, esize]);
    constant integer res = (element3 << esize) + (2 * element1 * element2);
    Elem[result, e, esize] = SignedSat((res + (1 << (esize - 1))) >> esize, esize);

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `sqrdmlah_z_zzz.xml`
</details>