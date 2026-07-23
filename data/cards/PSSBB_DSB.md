## DSB `[ALIAS]`
_ARM A64 Instruction_ (Alias of dsb.xml)

**Title**: PSSBB -- A64 | **Class**: `system` | **XML ID**: `PSSBB_DSB`

**Summary**: Physical speculative store bypass barrier

**Description**:
This instruction is a memory barrier that prevents speculative
loads from bypassing earlier stores to the same physical address under certain conditions.
For more information and details of the semantics, see
Physical Speculative Store Bypass Barrier (PSSBB).

### Variant: `Memory barrier`
- **Assembly**: `PSSBB`
- **Alias of**: `DSB  #4`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7  6   4  |
|-----------------------|
| 110 101 01000000110011 0100 1   00  11111 |
```

---
<details><summary>Metadata</summary>

- alias_mnemonic: `PSSBB`
- dsb-variants: `dsb-memory`
- isa: `A64`
- source: `pssbb_dsb.xml`
</details>