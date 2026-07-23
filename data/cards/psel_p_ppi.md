## PSEL
_ARM A64 Instruction_

**Title**: PSEL -- A64 | **Class**: `sve2` | **XML ID**: `psel_p_ppi`

**Architecture**: `FEAT_SME || FEAT_SVE2p1` (FEAT_SME || FEAT_SVE2p1)

**Summary**: Predicate select between predicate register or all-false

**Description**:
If the indexed element of the second source predicate is true,
place the contents of the first source predicate register into
the destination predicate register, otherwise set the destination
predicate to all-false.
The indexed element is determined by the sum of a general-purpose
index register and an immediate, modulo the number of elements.
Does not set the condition flags.

For programmer convenience, an assembler must
      also accept predicate-as-counter register names for the destination
      predicate register and the first source predicate register.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `PSEL  <Pd>, <Pn>, <Pm>.<T>[<Wv>, <imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  17  15  13   9  8   4  3  |
|--------------------------------------------|
| 001 0010 1   i1  tszh 1   tszl Rv  01  Pn  0   Pm  0   Pd  |
```

#### Decode (A64.sve.sve_pred_dup.sve_int_pred_dup.psel_p_ppi_)

```
if !IsFeatureImplemented(FEAT_SME) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant bits(5) imm5 = i1:tszh:tszl;
integer esize;
integer imm;
case tszh:tszl of
    when '0000' EndOfDecode(Decode_UNDEF);
    when '1000' esize = 64;  imm = UInt(imm5<4>);
    when 'x100' esize = 32;  imm = UInt(imm5<4:3>);
    when 'xx10' esize = 16;  imm = UInt(imm5<4:2>);
    when 'xxx1' esize = 8;   imm = UInt(imm5<4:1>);
constant integer n = UInt(Pn);
constant integer m = UInt(Pm);
constant integer d = UInt(Pd);
constant integer v = UInt('011':Rv);
```

#### Execute (A64.sve.sve_pred_dup.sve_int_pred_dup.psel_p_ppi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) operand1 = P[n, PL];
constant bits(PL) operand2 = P[m, PL];
constant bits(32) idx = X[v, 32];
constant integer element = (UInt(idx) + imm) MOD elements;
bits(PL) result;

if ActivePredicateElement(operand2, element, esize) then
    result = operand1;
else
    result = Zeros(PL);

P[d, PL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl != '0000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first source scalable predicate register, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second source scalable predicate register, encoded in the "Pm" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W12-W15, encoded in the "Rv" field. |
| `<imm>` | `immediate` | `i1:tszh:tszl` | Is the element index, in the range 0 to one less than the number of vector elements in a 128-bit vector register, encoded in "i1:tszh:tszl". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 000 | RESERVED |
| xx1 | B |
| x10 | H |
| 100 | S |
| 000 | D |

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

- isa: `A64`
- source: `psel_p_ppi.xml`
</details>