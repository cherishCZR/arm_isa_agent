"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ExternalLink, Play, Tags } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api/client";

type Encoding = { name: string; label: string; assembly_template: string; assembly_template_raw: string; bit_pattern: string; bitdiffs: string; operand_symbols: string[]; arch_variants: unknown[] };
type Instruction = {
  xml_id: string; mnemonic: string; title: string; brief: string; description: string; instruction_type: string; is_alias: boolean; alias_of: string; instr_class: string; source_file: string; is_predicated: boolean;
  category: { id: string; name: string; subcategory: { id: string; name: string } };
  features: string[]; operands: Array<{ symbol: string; description: string; type: string; register_class: string; register_width: number; encoding_name: string }>;
  constraints: Array<{ type: string; condition: string; description: string; encoding_name: string }>;
  encodings: Encoding[]; pseudocode: Array<{ name: string; section_type: string; body: string }>;
};
type Related = { xml_id: string; mnemonic: string; title: string; encoding_count: number };

export default function InstructionDetailPage() {
  const { xmlId } = useParams<{ xmlId: string }>();
  const router = useRouter();
  const [instruction, setInstruction] = useState<Instruction | null>(null);
  const [related, setRelated] = useState<Related[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.exploreInstruction(xmlId).then(setInstruction).catch(() => setError("Unable to load this XML instruction variant."));
    api.exploreRelatedVariants(xmlId).then((data) => setRelated(data.items ?? [])).catch(() => setRelated([]));
  }, [xmlId]);

  if (error) return <div className="max-w-5xl mx-auto"><Button variant="ghost" size="sm" onClick={() => router.push("/explore")}><ArrowLeft className="w-4 h-4" />Explore</Button><p className="mt-6 text-sm text-red-600">{error}</p></div>;
  if (!instruction) return <div className="max-w-5xl mx-auto text-sm text-muted-foreground py-12">Loading XML instruction profile...</div>;

  const categoryPath = `/explore/category/${encodeURIComponent(instruction.category.id)}`;
  const subcategoryPath = `${categoryPath}/${encodeURIComponent(instruction.category.subcategory.id)}`;
  return <div className="max-w-6xl mx-auto space-y-6">
    <div className="flex items-center justify-between gap-4"><Button variant="ghost" size="sm" className="-ml-2" onClick={() => router.push(subcategoryPath)}><ArrowLeft className="w-4 h-4" />Instruction directory</Button><Button size="sm" onClick={() => router.push(`/verify?instruction=${encodeURIComponent(instruction.xml_id)}`)}><Play className="w-4 h-4" />Verify this variant</Button></div>

    <section><p className="text-sm text-muted-foreground"><button onClick={() => router.push("/explore")} className="hover:underline">Knowledge Base</button> / <button onClick={() => router.push(categoryPath)} className="hover:underline">{instruction.category.name}</button> / <button onClick={() => router.push(subcategoryPath)} className="hover:underline">{instruction.category.subcategory.name}</button></p><div className="mt-3 flex flex-wrap items-baseline gap-x-4 gap-y-2"><h1 className="font-mono text-3xl font-bold">{instruction.mnemonic}</h1><span className="font-mono text-sm text-muted-foreground">{instruction.xml_id}</span>{instruction.is_alias && <Badge>Alias</Badge>}</div><p className="mt-2 text-lg">{instruction.title}</p>{instruction.brief && <p className="mt-3 max-w-4xl text-muted-foreground">{instruction.brief}</p>}</section>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4"><Card className="lg:col-span-2"><CardHeader className="pb-2"><CardTitle className="text-base">Architecture Profile</CardTitle></CardHeader><CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3 text-sm"><Property label="Category" value={instruction.category.name} /><Property label="Functional group" value={instruction.category.subcategory.name} /><Property label="XML instruction class" value={instruction.instr_class || "Not specified"} /><Property label="Source XML" value={instruction.source_file} />{instruction.is_alias && <Property label="Alias of" value={instruction.alias_of || "Architecture alias"} />}{instruction.is_predicated && <Property label="Execution" value="Predicated" />}</CardContent></Card><Card><CardHeader className="pb-2"><CardTitle className="text-base flex items-center gap-2"><Tags className="w-4 h-4" />Required Features</CardTitle></CardHeader><CardContent className="flex flex-wrap gap-1">{instruction.features.length ? instruction.features.map((feature) => <Badge key={feature} variant="secondary" className="font-mono">{feature}</Badge>) : <span className="text-sm text-muted-foreground">Base A64</span>}</CardContent></Card></div>

    <Card><CardHeader className="pb-2"><CardTitle className="text-base">Assembly Encodings</CardTitle><CardDescription>{instruction.encodings.length} encoding form(s) extracted from the ARM XML specification.</CardDescription></CardHeader><CardContent className="space-y-3">{instruction.encodings.map((encoding) => <div key={`${encoding.name}-${encoding.label}`} className="border rounded-md p-3"><div className="flex flex-wrap justify-between gap-2"><span className="font-mono font-semibold">{encoding.name}</span>{encoding.label && <Badge variant="outline">{encoding.label}</Badge>}</div><pre className="mt-3 overflow-x-auto rounded bg-muted px-3 py-2 text-xs">{encoding.assembly_template || encoding.assembly_template_raw || "Assembly template not present in XML."}</pre>{encoding.bit_pattern && <p className="mt-2 font-mono text-xs text-muted-foreground break-all">{encoding.bit_pattern}</p>}</div>)}</CardContent></Card>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4"><DataCard title="Operands" empty="No operand metadata is present for this XML variant.">{instruction.operands.map((operand, index) => <div key={`${operand.symbol}-${index}`} className="border-b last:border-0 py-2"><div className="flex gap-2 items-center"><span className="font-mono text-sm font-semibold">{operand.symbol}</span><Badge variant="outline">{operand.type}</Badge>{operand.register_class && <Badge variant="secondary">{operand.register_class}{operand.register_width ? ` ${operand.register_width}` : ""}</Badge>}</div>{operand.description && <p className="mt-1 text-xs text-muted-foreground">{operand.description}</p>}</div>)}</DataCard><DataCard title="Constraints" empty="No explicit operand constraints are present for this XML variant.">{instruction.constraints.map((constraint, index) => <div key={`${constraint.type}-${index}`} className="border-b last:border-0 py-2"><span className="font-mono text-sm font-semibold">{constraint.type || "constraint"}</span>{constraint.condition && <pre className="mt-1 whitespace-pre-wrap font-mono text-xs text-muted-foreground">{constraint.condition}</pre>}{constraint.description && <p className="mt-1 text-xs text-muted-foreground">{constraint.description}</p>}</div>)}</DataCard></div>

    {instruction.description && <Card><CardHeader className="pb-2"><CardTitle className="text-base">Description</CardTitle></CardHeader><CardContent><p className="whitespace-pre-wrap text-sm leading-6 text-muted-foreground">{instruction.description}</p></CardContent></Card>}
    {instruction.pseudocode.length > 0 && <Card><CardHeader className="pb-2"><CardTitle className="text-base">Architecture Pseudocode</CardTitle><CardDescription>Kept collapsed because ARM pseudocode can be substantial.</CardDescription></CardHeader><CardContent>{instruction.pseudocode.map((item, index) => <details key={`${item.name}-${index}`} className="border-b last:border-0 py-2"><summary className="cursor-pointer font-mono text-sm">{item.section_type}: {item.name}</summary><pre className="mt-3 max-h-96 overflow-auto rounded bg-muted p-3 text-xs">{item.body}</pre></details>)}</CardContent></Card>}
    {related.length > 0 && <Card><CardHeader className="pb-2"><CardTitle className="text-base">Related XML Variants</CardTitle><CardDescription>Variants that use the same mnemonic.</CardDescription></CardHeader><CardContent className="space-y-1">{related.map((item) => <button key={item.xml_id} type="button" onClick={() => router.push(`/explore/instruction/${encodeURIComponent(item.xml_id)}`)} className="w-full flex justify-between gap-4 rounded px-2 py-2 text-left hover:bg-muted/60"><span><span className="font-mono font-semibold">{item.mnemonic}</span><span className="ml-3 font-mono text-xs text-muted-foreground">{item.xml_id}</span></span><ExternalLink className="w-3 h-3 text-muted-foreground" /></button>)}</CardContent></Card>}
  </div>;
}

function Property({ label, value }: { label: string; value: string }) {
  return <div><p className="text-xs text-muted-foreground">{label}</p><p className="mt-1 font-mono text-sm break-all">{value}</p></div>;
}

function DataCard({ title, empty, children }: { title: string; empty: string; children: React.ReactNode }) {
  const hasChildren = Array.isArray(children) ? children.length > 0 : Boolean(children);
  return <Card><CardHeader className="pb-2"><CardTitle className="text-base">{title}</CardTitle></CardHeader><CardContent>{hasChildren ? children : <p className="text-sm text-muted-foreground">{empty}</p>}</CardContent></Card>;
}
