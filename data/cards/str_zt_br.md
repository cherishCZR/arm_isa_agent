## STR
_ARM A64 Instruction_

**Title**: STR (table) -- A64 | **Class**: `mortlach2` | **XML ID**: `str_zt_br`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Store ZT0 register

**Description**:
This instruction stores the 64-byte ZT0 register to the memory address provided in the 64-bit scalar
base register.
This instruction is unpredicated.

The store is performed as contiguous byte accesses, with no endian conversion
and no guarantee of single-copy atomicity larger than a byte.
However, if alignment is checked, then the base register must be aligned to 16 bytes.

This instruction does not require the PE to be in Streaming SVE mode,
and it is expected that this instruction will not experience a significant slowdown
due to contention with other PEs that are executing in Streaming SVE mode.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_1`

### Variant: `SME2`
- **Assembly**: `STR  ZT0, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  21  15 14   9   4   1  |
|--------------------------------|
| 1   11  0000 100 111111 1   00000 Rn  000 00  |
```

#### Decode (A64.sme.mortlach_mem.mortlach_zt_ldst.str_zt_br_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
```

#### Execute (A64.sme.mortlach_mem.mortlach_zt_ldst.str_zt_br_)

```
CheckSMEEnabled();
CheckSMEZT0Enabled();
constant integer elements = 512 DIV 8;
bits(64) addr;
constant bits(512) table = ZT0[512];
constant boolean contiguous = TRUE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
constant AccessDescriptor accdesc = CreateAccDescSME(MemOp_STORE, nontemporal, contiguous,
                                                     tagchecked);

if IsFeatureImplemented(FEAT_TME) && TSTATE.depth > 0 then
    FailTransaction(TMFailure_ERR, FALSE);

if n == 31 then
    CheckSPAlignment();
    addr = SP[64];
else
    addr = X[n, 64];

constant boolean aligned = IsAligned(addr, 16);

if !aligned && AlignmentEnforced() then
    constant FaultRecord fault = AlignmentFault(accdesc, addr);
    AArch64.Abort(fault);

for e = 0 to elements-1
    AArch64.MemSingle[addr, 1, accdesc, aligned] = Elem[table, e, 8];
    addr = AddressIncrement(addr, 1, accdesc);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `str_zt_br.xml`
</details>