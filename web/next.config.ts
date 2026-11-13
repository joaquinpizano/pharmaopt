import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  outputFileTracingIncludes: {
    "/api/packages": ["./data/pharmaopt_packages.csv.gz"],
  },
};

export default nextConfig;
