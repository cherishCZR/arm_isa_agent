"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ChevronRight, FolderTree } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { api } from "@/lib/api/client";

type Subcategory = { id: string; name: string; variant_count: number };
type Category = { id: string; name: string; variant_count: number; mnemonic_count: number; encoding_count: number; subcategories: Subcategory[] };

export default function CategoryDirectoryPage() {
  const { categoryId } = useParams<{ categoryId: string }>();
  const router = useRouter();
  const [category, setCategory] = useState<Category | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.exploreCategory(categoryId).then((data) => setCategory(data.category)).catch(() => setError("Unable to load this instruction category."));
  }, [categoryId]);

  return <div className="max-w-5xl mx-auto">
    <Button variant="ghost" size="sm" className="mb-5 -ml-2" onClick={() => router.push("/explore")}><ArrowLeft className="w-4 h-4" />All categories</Button>
    {error && <p className="text-sm text-red-600">{error}</p>}
    {category && <>
      <div className="mb-7">
        <p className="text-sm text-muted-foreground mb-2">Instruction Knowledge Base / Functional Categories</p>
        <h1 className="text-2xl font-bold">{category.name}</h1>
        <p className="text-muted-foreground mt-2">{category.variant_count} XML variants, {category.mnemonic_count} mnemonics, and {category.encoding_count} encodings.</p>
      </div>
      <section>
        <div className="flex items-center gap-2 mb-3"><FolderTree className="w-4 h-4" /><h2 className="font-semibold">Functional Subcategories</h2></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {category.subcategories.map((subcategory) => <Card key={subcategory.id} className="rounded-md hover:bg-muted/40 transition-colors cursor-pointer" onClick={() => router.push(`/explore/category/${encodeURIComponent(category.id)}/${encodeURIComponent(subcategory.id)}`)}>
            <CardContent className="p-4 flex items-center justify-between gap-4">
              <div><p className="font-medium">{subcategory.name}</p><p className="font-mono text-xs text-muted-foreground mt-1">{subcategory.id}</p></div>
              <div className="flex items-center gap-3"><Badge variant="outline">{subcategory.variant_count} variants</Badge><ChevronRight className="w-4 h-4 text-muted-foreground" /></div>
            </CardContent>
          </Card>)}
        </div>
      </section>
    </>}
  </div>;
}
