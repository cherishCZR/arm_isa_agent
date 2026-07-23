"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpRight, BookOpen, Database, Search } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api/client";

type Category = {
  id: string;
  name: string;
  variant_count: number;
  mnemonic_count: number;
  encoding_count: number;
  subcategories: Array<{ id: string; variant_count: number }>;
};

type Variant = {
  xml_id: string;
  mnemonic: string;
  title: string;
  primary_category: string;
  subcategory: string;
  encoding_count: number;
  features: string[];
  operand_classes: string[];
  is_alias: boolean;
};

type Taxonomy = {
  taxonomy_version: string;
  coverage: {
    xml_variants: number;
    classified_variants: number;
    unclassified_variants: number;
    encodings: number;
    coverage_complete: boolean;
  };
  categories: Category[];
};

export default function ExplorePage() {
  const [taxonomy, setTaxonomy] = useState<Taxonomy | null>(null);
  const [variants, setVariants] = useState<Variant[]>([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    api.exploreTaxonomy().then(setTaxonomy).catch(() => setError("Unable to load instruction taxonomy."));
  }, []);

  useEffect(() => {
    api.exploreVariants({ search, page, pageSize: 50 })
      .then((response) => {
        setVariants(response.items ?? []);
        setTotal(response.total ?? 0);
      })
      .catch(() => setError("Unable to load XML instruction variants."));
  }, [search, page]);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-7">
        <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Database className="w-6 h-6" />Instruction Knowledge Base</h1>
        <p className="text-muted-foreground">XML-variant taxonomy derived from the ARM A64 ISA specification.</p>
      </div>

      {taxonomy && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          <Metric label="XML variants" value={`${taxonomy.coverage.classified_variants}/${taxonomy.coverage.xml_variants}`} />
          <Metric label="Encodings" value={String(taxonomy.coverage.encodings)} />
          <Metric label="Unclassified" value={String(taxonomy.coverage.unclassified_variants)} danger={taxonomy.coverage.unclassified_variants > 0} />
          <Metric label="Taxonomy" value={taxonomy.taxonomy_version} />
        </div>
      )}

      <div className="relative mb-5">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input placeholder="Search mnemonic, XML variant, or title..." value={search} onChange={(event) => { setSearch(event.target.value); setPage(1); }} className="pl-10 font-mono" />
      </div>

      {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

      <section className="mb-8">
        <div className="flex items-center justify-between mb-3"><h2 className="font-semibold">Functional Categories</h2><Button size="sm" onClick={() => document.getElementById("all-variants")?.scrollIntoView({ behavior: "smooth" })}>All variants</Button></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {taxonomy?.categories.filter((category) => category.variant_count > 0).map((category) => (
            <button key={category.id} type="button" onClick={() => router.push(`/explore/category/${encodeURIComponent(category.id)}`)} className="text-left border rounded-md p-4 transition-colors hover:bg-muted/40">
              <div className="flex justify-between gap-3"><span className="font-medium">{category.name}</span><Badge variant="outline">{category.variant_count} variants</Badge></div>
              <p className="text-xs text-muted-foreground mt-1">{category.mnemonic_count} mnemonics · {category.encoding_count} encodings</p>
              <div className="flex flex-wrap gap-1 mt-3">{category.subcategories.slice(0, 4).map((subcategory) => <Badge key={subcategory.id} variant="secondary" className="text-[10px]">{subcategory.id.replaceAll("_", " ")} {subcategory.variant_count}</Badge>)}</div>
            </button>
          ))}
        </div>
      </section>

      <Card id="all-variants">
        <CardHeader className="pb-2"><CardTitle className="text-base flex gap-2 items-center"><BookOpen className="w-4 h-4" />XML Instruction Variants</CardTitle><CardDescription>{total} matching variants. Counts use XML variants, not only mnemonics.</CardDescription></CardHeader>
        <CardContent className="space-y-1">
          {variants.map((variant) => (
            <button key={variant.xml_id} type="button" onClick={() => router.push(`/explore/instruction/${encodeURIComponent(variant.xml_id)}`)} className="w-full grid grid-cols-[minmax(80px,0.55fr)_minmax(150px,1.2fr)_minmax(0,2fr)_auto] gap-3 items-center text-left px-3 py-2 rounded hover:bg-muted/60">
              <span className="font-mono font-semibold truncate">{variant.mnemonic}</span>
              <span className="font-mono text-xs text-muted-foreground truncate">{variant.xml_id}</span>
              <span className="text-xs text-muted-foreground truncate">{variant.title}</span>
              <ArrowUpRight className="w-3 h-3 opacity-40" />
            </button>
          ))}
          {variants.length === 0 && <p className="text-sm text-muted-foreground py-6 text-center">No XML instruction variants match this filter.</p>}
          <div className="flex justify-between pt-3"><Button variant="outline" size="sm" disabled={page === 1} onClick={() => setPage((value) => value - 1)}>Previous</Button><span className="text-xs text-muted-foreground self-center">Page {page} · {total} variants</span><Button variant="outline" size="sm" disabled={page * 50 >= total} onClick={() => setPage((value) => value + 1)}>Next</Button></div>
        </CardContent>
      </Card>
    </div>
  );
}

function Metric({ label, value, danger = false }: { label: string; value: string; danger?: boolean }) {
  return <Card><CardContent className="p-3"><p className="text-xs text-muted-foreground">{label}</p><p className={`font-mono text-lg mt-1 ${danger ? "text-red-600" : ""}`}>{value}</p></CardContent></Card>;
}
