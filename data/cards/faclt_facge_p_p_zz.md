## FACGT `[ALIAS]`
_ARM A64 Instruction_ (Alias of facge_p_p_zz.xml)

**Title**: FACLT -- A64 | **Class**: `sve` | **XML ID**: `faclt_facge_p_p_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point absolute compare less than

**Description**:
Compare active absolute values of floating-point elements in the
first source vector being less than corresponding absolute values of elements in the second source vector, and
place the boolean results of the 
comparison in the corresponding elements of the destination
predicate.  Inactive elements in the destination predicate register are set to zero. Does not set the condition flags.

**Attributes**: Predicated

### Variant: `Greater than`
- **Assembly**: `FACLT  <Pd>.<T>, <Pg>/Z, <Zm>.<T>, <Zn>.<T>`
- **Alias of**: `FACGT  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
  Condition: Never
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 0   Zm  1   1   1   Pg  Zn  1   Pd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the predicate register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- alias_mnemonic: `FACLT`
- isa: `A64`
- sve-compare-type: `gt`
- source: `faclt_facge_p_p_zz.xml`
</details>