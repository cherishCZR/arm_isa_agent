"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ArrowUpRight, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api/client";

type Variant = { xml_id: string; mnemonic: string; title: string; encoding_count: number; features: string[] };
type Directory = { category: { id: string; name: string }; subcategory: { id: string; name: string; variant_count: number }; items: Variant[]; total: number; page: number; page_size: number };

export default function SubcategoryDirectoryPage() {
  const { categoryId, subcategoryId } = useParams<{ categoryId: string; subcategoryId: string }>();
  const router = useRouter();
  const [data, setData] = useState<Directory | null>(null);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");

  useEffect(() => {
    api.exploreSubcategory(categoryId, subcategoryId, { search, page, pageSize: 50 }).then(setData).catch(() => setError("Unable to load this instruction directory."));
  }, [categoryId, subcategoryId, search, page]);

  return <div className="max-w-6xl mx-auto">
    <Button variant="ghost" size="sm" className="mb-5 -ml-2" onClick={() => router.push(`/explore/category/${encodeURIComponent(categoryId)}`)}><ArrowLeft className="w-4 h-4" />Category directory</Button>
    {error && <p className="text-sm text-red-600">{error}</p>}
    {data && <>
      <div className="mb-6"><p className="text-sm text-muted-foreground mb-2">{data.category.name}</p><h1 className="text-2xl font-bold">{data.subcategory.name}</h1><p className="text-muted-foreground mt-2">{data.total} XML instruction variants.</p></div>
      <div className="relative mb-4"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" /><Input className="pl-10 font-mono" placeholder="Search this subcategory..." value={search} onChange={(event) => { setSearch(event.target.value); setPage(1); }} /></div>
      <Card><CardHeader className="pb-2"><CardTitle className="text-base">Instruction Variants</CardTitle><CardDescription>Each entry is a source XML variant and opens its ARM specification profile.</CardDescription></CardHeader><CardContent className="space-y-1">
        {data.items.map((variant) => <button key={variant.xml_id} type="button" onClick={() => router.push(`/explore/instruction/${encodeURIComponent(variant.xml_id)}`)} className="w-full grid grid-cols-[minmax(84px,.5fr)_minmax(170px,1.1fr)_minmax(0,2fr)_auto] gap-3 items-center text-left px-3 py-2 rounded hover:bg-muted/60"><span className="font-mono font-semibold truncate">{variant.mnemonic}</span><span className="font-mono text-xs text-muted-foreground truncate">{variant.xml_id}</span><span className="text-xs text-muted-foreground truncate">{variant.title}</span><ArrowUpRight className="w-3 h-3 opacity-40" /></button>)}
        {data.items.length === 0 && <p className="text-sm text-muted-foreground py-6 text-center">No XML instruction variants match this filter.</p>}
        <div className="flex justify-between pt-3"><Button variant="outline" size="sm" disabled={page === 1} onClick={() => setPage((value) => value - 1)}>Previous</Button><span className="self-center text-xs text-muted-foreground">Page {page} of {data.total} variants</span><Button variant="outline" size="sm" disabled={page * data.page_size >= data.total} onClick={() => setPage((value) => value + 1)}>Next</Button></div>
      </CardContent></Card>
    </>}
  </div>;
}
