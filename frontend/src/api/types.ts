export type CommonResponse<T> = {
  status: number;
  message: string;
  data: T | null;
};

export type ServiceHealthData = {
  name: string;
  version: string;
  environment: string;
  api_prefix: string;
  time_zone: string;
  db_enabled: boolean;
  response_at: string;
};

export type ClassAnalysisItem = {
  class_name: string;
  homework_deduction: number;
  daily_deduction: number;
  late_deduction: number;
};

export type StudentAnalysisItem = {
  student_name: string;
  total_add_score: number;
  rank: number;
  bonus_details: string;
};

export type BypAnalysisData = {
  response_at: string;
  class_stat: ClassAnalysisItem[];
  student_stat: StudentAnalysisItem[];
};
