## MOVPRFX
_ARM A64 Instruction_

**Title**: MOVPRFX (predicated) -- A64 | **Class**: `sve` | **XML ID**: `movprfx_z_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Move prefix (predicated)

**Description**:
The predicated MOVPRFX instruction is a hint to hardware that the instruction
may be combined with the destructive instruction which
follows it in program order to create a single constructive
operation.  Since it is a hint it is also
permitted to be implemented as a discrete vector copy, and
the result of executing the pair of instructions with or
without combining is identical. The choice of combined
versus discrete operation may vary dynamically.

Unless the combination of a constructive operation with
   merging predication is specifically required, it is strongly
   recommended that for performance reasons software should
   prefer to use the zeroing form of predicated MOVPRFX or
   the unpredicated MOVPRFX instruction.

Although the operation of the instruction is defined as a
simple predicated vector copy, it is required that the prefixed
instruction at PC+4 must be an SVE destructive
binary or ternary instruction encoding, or a unary operation with
merging predication, but excluding other MOVPRFX
instructions.
The prefixed instruction must specify
the same predicate register, and  have the same maximum element size
  (ignoring a fixed 64-bit "wide vector" operand), and the same destination vector as the MOVPRFX instruction.
The prefixed instruction must not use the
destination register in any other operand position,
even if they have different names but refer to the
same architectural register state.
Any other use is UNPREDICTABLE.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `MOVPRFX  <Zd>.<T>, <Pg>/<ZM>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  12   9   4  |
|--------------------------------------|
| 000 0010 0   size 0   10  00  M   001 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_red.sve_int_movprfx_pred.movprfx_z_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = (M == '1');
```

#### Execute (A64.sve.sve_int_pred_red.sve_int_movprfx_pred.movprfx_z_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
constant bits(VL) dest = if merging then Z[d, VL] else Zeros(VL);
bits(VL) result;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand1, e, esize];
        Elem[result, e, esize] = element;
    else
        Elem[result, e, esize] = Elem[dest, e, esize];

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<ZM>` | `register (128-bit)` | `M` | Is the predication qualifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<ZM> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | Z |
| 1 | M |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `movprfx_z_p_z.xml`
</details>