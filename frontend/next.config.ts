import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Allow images from any source (for instruction icons, etc.)
  images: {
    remotePatterns: [{ protocol: "https", hostname: "**" }],
  },
};

export default nextConfig;
