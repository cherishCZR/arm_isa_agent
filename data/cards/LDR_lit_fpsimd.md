## LDR
_ARM A64 Instruction_

**Title**: LDR (literal, SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `LDR_lit_fpsimd`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Load SIMD&FP register (PC-relative literal)

**Description**:
This instruction loads a SIMD&FP register from memory.
The address that is used for the load is calculated from the PC value
and an immediate offset.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Literal (LDR_S_loadlit)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `LDR  <St>, <label>`
- **Fixed bits**: `opc`=`00`
- **Bit Pattern**: `??????????????????????????????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23   4  |
|--------------------|
| opc 011 1   00  imm19 Rt  |
```

#### Decode (A64.ldst.loadlit.LDR_S_loadlit)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
if opc == '11' then EndOfDecode(Decode_UNDEF);
constant integer size = 4 << (UInt(opc));
constant boolean nontemporal = FALSE;
constant boolean tagchecked = FALSE;

constant bits(64) offset = SignExtend(imm19:'00', 64);
```

#### Execute (A64.ldst.loadlit.LDR_S_loadlit)

```
constant bits(64) address = PC64 + offset;
CheckFPEnabled64();
constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_LOAD, nontemporal,
                                                       tagchecked, privileged);
constant bits(size*8) data = Mem[address, size, accdesc];
V[t, size*8] = data;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `opc != '11'` |

### Variant: `Literal (LDR_D_loadlit)` (64-bit)
- **Condition**: `opc == 01`
- **Assembly**: `LDR  <Dt>, <label>`
- **Fixed bits**: `opc`=`01`
- **Bit Pattern**: `??????????????????????????????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23   4  |
|--------------------|
| opc 011 1   00  imm19 Rt  |
```

### Variant: `Literal (LDR_Q_loadlit)` (128-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDR  <Qt>, <label>`
- **Fixed bits**: `opc`=`10`
- **Bit Pattern**: `??????????????????????????????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23   4  |
|--------------------|
| opc 011 1   00  imm19 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<St>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |
| `<label>` | `label` | `imm19` | Is the program label from which the data is to be loaded. Its offset from the address of this instruction, in the range +/-1MB, is encoded as "imm19"  |
| `<Dt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |
| `<Qt>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `literal`
- isa: `A64`
- offset-type: `off19s`
- source: `ldr_lit_fpsimd.xml`
</details>