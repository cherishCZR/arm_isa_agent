## DMB
_ARM A64 Instruction_

**Title**: DMB -- A64 | **Class**: `system` | **XML ID**: `DMB`

**Summary**: Data memory barrier

**Description**:
This instruction is a memory barrier that ensures the ordering
of observations of memory accesses, see Data Memory Barrier.

### Variant: `System`
- **Assembly**: `DMB  (<option>|#<imm>)`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7  6   4  |
|-----------------------|
| 110 101 01000000110011 CRm 1   01  11111 |
```

#### Decode (A64.control.barriers.DMB_BO_barriers)

```
MBReqDomain domain;
MBReqTypes types;
case CRm<3:2> of
    when '00' domain = MBReqDomain_OuterShareable;
    when '01' domain = MBReqDomain_Nonshareable;
    when '10' domain = MBReqDomain_InnerShareable;
    when '11' domain = MBReqDomain_FullSystem;
case CRm<1:0> of
    when '00' types = MBReqTypes_All; domain = MBReqDomain_FullSystem;
    when '01' types = MBReqTypes_Reads;
    when '10' types = MBReqTypes_Writes;
    when '11' types = MBReqTypes_All;
```

#### Execute (A64.control.barriers.DMB_BO_barriers)

```
DataMemoryBarrier(domain, types);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<option>` | `unknown` | `CRm` | Specifies the limitation on the barrier operation. Values are:                                       SY               Full system is the required shar |
| `<imm>` | `immediate` | `CRm` | Is a 4-bit unsigned immediate, in the range 0 to 15, encoded in the "CRm" field. |

**<option> Value Table**:

| bitfield | symbol |
|---|---|
| xx00 | RESERVED |
| 0001 | OSHLD |
| 0010 | OSHST |
| 0011 | OSH |
| 0101 | NSHLD |
| 0110 | NSHST |
| 0111 | NSH |
| 1001 | ISHLD |
| 1010 | ISHST |
| 1011 | ISH |
| 1101 | LD |
| 1110 | ST |
| 1111 | SY |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `dmb.xml`
</details>