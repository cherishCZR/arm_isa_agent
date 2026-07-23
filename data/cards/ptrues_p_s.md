## PTRUES
_ARM A64 Instruction_

**Title**: PTRUES -- A64 | **Class**: `sve` | **XML ID**: `ptrues_p_s`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Initialise predicate from named constraint and set the condition flags

**Description**:
Set elements of the destination predicate to true if the
element number satisfies the named predicate constraint,
or to false otherwise.  If the constraint specifies more
elements than are available at the current vector length
then all elements of the destination predicate are set to
false.

The named predicate constraint limits the number of active
elements in a single predicate to:

Unspecified or out of range constraint encodings generate an
empty predicate or zero element count rather than Undefined
Instruction exception. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Setting the condition flags`
- **Assembly**: `PTRUES  <Pd>.<T>{, <pattern>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  16 15  13  10  9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 01  100 1   11  100 0   pattern 0   Pd  |
```

#### Decode (A64.sve.sve_pred_gen_d.sve_int_ptrue.ptrues_p_s_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer d = UInt(Pd);
constant boolean setflags = TRUE;
constant bits(5) pat = pattern;
```

#### Execute (A64.sve.sve_pred_gen_d.sve_int_ptrue.ptrues_p_s_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant integer count = DecodePredCount(pat, esize);
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    constant bit pbit = if e < count then '1' else '0';
    Elem[result, e, psize] = ZeroExtend(pbit, psize);

if setflags then
    PSTATE.<N,Z,C,V> = PredTest(result, result, esize);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<pattern>` | `unknown` | `pattern` | Is the optional pattern specifier, defaulting to ALL, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<pattern> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 | POW2 |
| 00001 | VL1 |
| 00010 | VL2 |
| 00011 | VL3 |
| 00100 | VL4 |
| 00101 | VL5 |
| 00110 | VL6 |
| 00111 | VL7 |
| 01000 | VL8 |
| 01001 | VL16 |
| 01010 | VL32 |
| 01011 | VL64 |
| 01100 | VL128 |
| 01101 | VL256 |
| 0111x | #uimm5 |
| 1xx00 | #uimm5 |
| 1x0x1 | #uimm5 |
| 1x010 | #uimm5 |
| 101x1 | #uimm5 |
| 10110 | #uimm5 |
| 11101 | MUL4 |
| 11110 | MUL3 |
| 11111 | ALL |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- cond-setting: `s`
- isa: `A64`
- source: `ptrues_p_s.xml`
</details>