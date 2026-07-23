## LDUR
_ARM A64 Instruction_

**Title**: LDUR (SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `LDUR_fpsimd`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Load SIMD&FP register (unscaled offset)

**Description**:
This instruction loads a SIMD&FP register from memory.
The address that is used for the load is calculated from a base register value
and an optional immediate offset.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Unscaled offset (LDUR_B_ldst_unscaled)` (8-bit)
- **Condition**: `size == 00 && opc == 01`
- **Assembly**: `LDUR  <Bt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`00`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x1  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unscaled.LDUR_B_ldst_unscaled)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if opc<1> == '1' && size != '00' then EndOfDecode(Decode_UNDEF);
constant integer scale = if opc<1> == '1' then 4 else UInt(size);
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unscaled.LDUR_B_ldst_unscaled)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 8 << scale;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unscaled.LDUR_B_ldst_unscaled)

```
CheckFPEnabled64();
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_LOAD, nontemporal, tagchecked,
                                                       privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

V[t, datasize] = Mem[address, datasize DIV 8, accdesc];
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `opc<1> != '1' \|\| size == '00'` |

### Variant: `Unscaled offset (LDUR_H_ldst_unscaled)` (16-bit)
- **Condition**: `size == 01 && opc == 01`
- **Assembly**: `LDUR  <Ht>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`01`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x1  0   imm9 00  Rn  Rt  |
```

### Variant: `Unscaled offset (LDUR_S_ldst_unscaled)` (32-bit)
- **Condition**: `size == 10 && opc == 01`
- **Assembly**: `LDUR  <St>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`10`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x1  0   imm9 00  Rn  Rt  |
```

### Variant: `Unscaled offset (LDUR_D_ldst_unscaled)` (64-bit)
- **Condition**: `size == 11 && opc == 01`
- **Assembly**: `LDUR  <Dt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`11`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x1  0   imm9 00  Rn  Rt  |
```

### Variant: `Unscaled offset (LDUR_Q_ldst_unscaled)` (128-bit)
- **Condition**: `size == 00 && opc == 11`
- **Assembly**: `LDUR  <Qt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`00`, `opc`=`1`
- **Bit Pattern**: `???????????????????????1??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x1  0   imm9 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Bt>` | `register (8-bit)` | `Rt` | Is the 8-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |
| `<Ht>` | `register (16-bit)` | `Rt` | Is the 16-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<St>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Dt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- isa: `A64`
- offset-type: `off9s_u`
- source: `ldur_fpsimd.xml`
</details>