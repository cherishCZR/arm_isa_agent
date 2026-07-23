## MOVT
_ARM A64 Instruction_

**Title**: MOVT (vector to table) -- A64 | **Class**: `mortlach2` | **XML ID**: `movt_zt_z`

**Architecture**: `FEAT_SME_LUTv2` (ARMv9.5)

**Summary**: Move vector register to ZT0

**Description**:
This instruction copies the source vector register to ZT0 at the vector length offset
specified by the immediate index. When the index is zero, the instruction
writes zeroes to the most significant (512-VL) bits of the ZT0 register.
When the index is not zero, the unindexed portions of ZT0 remain unchanged.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `MOVT  ZT0{[<offs>, MUL VL]}, <Zt>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17 16  14 13  11   4  |
|--------------------------------|
| 1   10  0000 0010011 1   10  0   off2 0011111 Zt  |
```

#### Decode (A64.sme.mortlach_mov_zt.mortlach_move_to_zt.movt_zt_z_)

```
if !IsFeatureImplemented(FEAT_SME_LUTv2) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Zt);
constant integer imm = UInt(off2);
```

#### Execute (A64.sme.mortlach_mov_zt.mortlach_move_to_zt.movt_zt_z_)

```
CheckStreamingSVEEnabled();
CheckSMEZT0Enabled();
constant integer VL = CurrentVL;
constant integer tsize = if VL <= 512 then VL else 512;
constant integer offset = imm MOD (512 DIV tsize);
bits(512) result = if imm == 0 then Zeros(512) else ZT0[512];

Elem[result, offset, tsize] = Z[t, VL]<tsize-1:0>;
ZT0[512] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_LUTv2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<offs>` | `unknown` | `off2` | Is the vector length offset, in the range 0 to 3, defaulting to 0 when omitted, encoded in the "off2" field. |
| `<Zt>` | `register (128-bit)` | `Zt` | Is the name of the scalable vector register to be transferred, encoded in the "Zt" field. |

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
- source: `movt_zt_z.xml`
</details>