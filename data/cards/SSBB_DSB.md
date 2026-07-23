## DSB `[ALIAS]`
_ARM A64 Instruction_ (Alias of dsb.xml)

**Title**: SSBB -- A64 | **Class**: `system` | **XML ID**: `SSBB_DSB`

**Summary**: Speculative store bypass barrier

**Description**:
This instruction is a memory barrier that prevents speculative loads
from bypassing earlier stores to the same virtual address under certain conditions. For more
information and details of the semantics,
see Speculative Store Bypass Barrier (SSBB).

### Variant: `Memory barrier`
- **Assembly**: `SSBB`
- **Alias of**: `DSB  #0`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7  6   4  |
|-----------------------|
| 110 101 01000000110011 0000 1   00  11111 |
```

---
<details><summary>Metadata</summary>

- alias_mnemonic: `SSBB`
- dsb-variants: `dsb-memory`
- isa: `A64`
- source: `ssbb_dsb.xml`
</details>