## ADR
_ARM A64 Instruction_

**Title**: ADR -- A64 | **Class**: `sve` | **XML ID**: `adr_z_az`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Compute vector address

**Description**:
Optionally sign or zero-extend the least significant 32 bits
of each element from a vector of offsets or indices in the
second source vector, scale each index by 2, 4 or 8, add
to a vector of base addresses from the first source vector,
and place the resulting addresses in the destination
vector. This instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `Packed offsets`
- **Assembly**: `ADR  <Zd>.<T>, [<Zn>.<T>, <Zm>.<T>{, <mod> <amount>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  11   9   4  |
|-----------------------------------|
| 000 0010 0   1   sz  1   Zm  1010 msz Zn  Zd  |
```

#### Decode (A64.sve.sve_int_adr.sve_int_bin_cons_misc_0_a.adr_z_az_sd_same_scaled)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer osize = esize;
constant boolean unsigned = TRUE;
constant integer mbytes = 1 << UInt(msz);
```

#### Execute (A64.sve.sve_int_adr.sve_int_bin_cons_misc_0_a.adr_z_az_sd_same_scaled)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) base = Z[n, VL];
constant bits(VL) offs = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) addr = Elem[base, e, esize];
    constant integer offset = Int(Elem[offs, e, esize]<osize-1:0>, unsigned);
    Elem[result, e, esize] = addr + (offset * mbytes);

Z[d, VL] = result;
```

### Variant: `Unpacked 32-bit signed offsets`
- **Assembly**: `ADR  <Zd>.D, [<Zn>.D, <Zm>.D, SXTW{<amount>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 000 0010 0   00  1   Zm  1010 msz Zn  Zd  |
```

#### Decode (A64.sve.sve_int_adr.sve_int_bin_cons_misc_0_a.adr_z_az_d_s32_scaled)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer osize = 32;
constant boolean unsigned = FALSE;
constant integer mbytes = 1 << UInt(msz);
```

### Variant: `Unpacked 32-bit unsigned offsets`
- **Assembly**: `ADR  <Zd>.D, [<Zn>.D, <Zm>.D, UXTW{<amount>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 000 0010 0   01  1   Zm  1010 msz Zn  Zd  |
```

#### Decode (A64.sve.sve_int_adr.sve_int_bin_cons_misc_0_a.adr_z_az_d_u32_scaled)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer osize = 32;
constant boolean unsigned = TRUE;
constant integer mbytes = 1 << UInt(msz);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `sz` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the base scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the offset scalable vector register, encoded in the "Zm" field. |
| `<mod>` | `unknown` | `msz` | Is the index extend and shift specifier, |
| `<amount>` | `unknown` | `msz` | Is the index shift amount, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

**<mod> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | [absent] |
| x1 | LSL |
| 10 | LSL |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | [absent] |
| 01 | #1 |
| 10 | #2 |
| 11 | #3 |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |

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
- source: `adr_z_az.xml`
</details>