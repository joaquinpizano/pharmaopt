export type PackageRecord = {
  package_ndc: string;
  generic_name: string;
  brand_name: string;
  labeler_name: string;
  dosage_form: string;
  marketing_category: string;
  package_description: string;
  risk_score_v04: number;
  risk_score_v05: number;
  fda_event_any: number;
  non_discontinuation_event_candidate: number;
  discontinuation_notice_candidate: number;
  risk_rank: number;
};

export type PackageResponse = {
  rows: PackageRecord[];
  total: number;
  page: number;
  pageSize: number;
  model: "v04" | "v05";
};
