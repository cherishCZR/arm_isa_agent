## TBX
_ARM A64 Instruction_

**Title**: TBX -- A64 | **Class**: `advsimd` | **XML ID**: `TBX_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Table vector lookup extension

**Description**:
This instruction reads each value from the vector elements in the index source SIMD&FP register,
uses each result as an index to perform a lookup in a table of bytes that
is described by one to four source table SIMD&FP registers,
places the lookup result in a vector, and writes
the vector to the destination SIMD&FP register.
If an index is out of range for the table, the existing value in the vector element
of the destination register is left unchanged.
If more than one source register is used to describe the table,
the first source register describes the lowest bytes of the table.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD (TBX_asimdtbl_L1_1)` (Single register table)
- **Condition**: `len == 00`
- **Assembly**: `TBX  <Vd>.<Ta>, { <Vn>.16B }, <Vm>.<Ta>`
- **Fixed bits**: `len`=`00`
- **Bit Pattern**: `?????????????00?????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   Q   001110 00  0   Rm  0   len 1   00  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdtbl.TBX_asimdtbl_L1_1)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV 8;
constant integer regs = UInt(len) + 1;
constant boolean is_tbl = (op == '0');
```

#### Execute (A64.simd_dp.asimdtbl.TBX_asimdtbl_L1_1)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) indices = V[m, datasize];
bits(128*regs) table = Zeros(128*regs);
bits(datasize) result;
integer index;

// Create table from registers
for i = 0 to regs - 1
    Elem[table, i, 128] = V[(n+i) MOD 32, 128];

result = if is_tbl then Zeros(datasize) else V[d, datasize];
for i = 0 to elements - 1
    index = UInt(Elem[indices, i, 8]);
    if index < 16 * regs then
        Elem[result, i, 8] = Elem[table, index, 8];

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Variant: `Advanced SIMD (TBX_asimdtbl_L2_2)` (Two register table)
- **Condition**: `len == 01`
- **Assembly**: `TBX  <Vd>.<Ta>, { <Vn>.16B, <Vn+1>.16B }, <Vm>.<Ta>`
- **Fixed bits**: `len`=`01`
- **Bit Pattern**: `?????????????10?????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   Q   001110 00  0   Rm  0   len 1   00  Rn  Rd  |
```

### Variant: `Advanced SIMD (TBX_asimdtbl_L3_3)` (Three register table)
- **Condition**: `len == 10`
- **Assembly**: `TBX  <Vd>.<Ta>, { <Vn>.16B, <Vn+1>.16B, <Vn+2>.16B }, <Vm>.<Ta>`
- **Fixed bits**: `len`=`10`
- **Bit Pattern**: `?????????????01?????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   Q   001110 00  0   Rm  0   len 1   00  Rn  Rd  |
```

### Variant: `Advanced SIMD (TBX_asimdtbl_L4_4)` (Four register table)
- **Condition**: `len == 11`
- **Assembly**: `TBX  <Vd>.<Ta>, { <Vn>.16B, <Vn+1>.16B, <Vn+2>.16B, <Vn+3>.16B }, <Vm>.<Ta>`
- **Fixed bits**: `len`=`11`
- **Bit Pattern**: `?????????????11?????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   Q   001110 00  0   Rm  0   len 1   00  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | For the "Single register table" variant: is the name of the SIMD&FP table register, encoded in the "Rn" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | For the "Four register table", "Three register table", and "Two register table" variants: is the name of the first SIMD&FP table register, encoded in  |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the SIMD&FP index register, encoded in the "Rm" field. |
| `<Vn+1>` | `register (128-bit)` | `Rn` | Is the name of the second SIMD&FP table register, encoded as "Rn" plus 1 modulo 32. |
| `<Vn+2>` | `register (128-bit)` | `Rn` | Is the name of the third SIMD&FP table register, encoded as "Rn" plus 2 modulo 32. |
| `<Vn+3>` | `register (128-bit)` | `Rn` | Is the name of the fourth SIMD&FP table register, encoded as "Rn" plus 3 modulo 32. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

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
- source: `tbx_advsimd.xml`
</details>