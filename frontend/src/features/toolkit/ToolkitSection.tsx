import { Alert, Button, Card, Empty, Input, Space, Spin, Table, Tag, Typography, message } from "antd";
import { useEffect, useState } from "react";

import { analyzeByp, fetchServiceHealth } from "../../api/client";
import type {
  BypAnalysisData,
  ClassAnalysisItem,
  ServiceHealthData,
  StudentAnalysisItem,
} from "../../api/types";
import { env } from "../../env";
import type { ToolkitTabKey } from "../../app/types";

const defaultExcelUrl = "";

type ToolkitSectionProps = {
  activeTab: ToolkitTabKey;
};

export function ToolkitSection({ activeTab }: ToolkitSectionProps) {
  const [health, setHealth] = useState<ServiceHealthData | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState<string | null>(null);

  const [excelUrl, setExcelUrl] = useState(defaultExcelUrl);
  const [analysis, setAnalysis] = useState<BypAnalysisData | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadHealth() {
      setHealthLoading(true);
      setHealthError(null);
      try {
        const response = await fetchServiceHealth();
        if (!active) {
          return;
        }
        setHealth(response.data ?? null);
      } catch (error) {
        if (!active) {
          return;
        }
        const messageText = error instanceof Error ? error.message : "服务状态获取失败";
        setHealthError(messageText);
      } finally {
        if (active) {
          setHealthLoading(false);
        }
      }
    }

    void loadHealth();
    return () => {
      active = false;
    };
  }, []);

  async function handleAnalyze() {
    if (!excelUrl.trim()) {
      message.warning("请先输入 Excel URL");
      return;
    }
    setAnalysisLoading(true);
    setAnalysisError(null);
    try {
      const response = await analyzeByp(excelUrl.trim());
      setAnalysis(response.data ?? null);
      message.success("分析完成");
    } catch (error) {
      const messageText = error instanceof Error ? error.message : "分析失败";
      setAnalysisError(messageText);
      setAnalysis(null);
    } finally {
      setAnalysisLoading(false);
    }
  }

  function renderHealthCard(extraClassName?: string) {
    const className = ["panel-card", "status-card", extraClassName].filter(Boolean).join(" ");

    return (
      <Card className={className} bordered={false}>
        <div className="status-card-head">
          <div>
            <h3>Service Health</h3>
            <p>来自 `/api/v1/system/health`</p>
          </div>
          <Button onClick={() => window.location.reload()}>刷新</Button>
        </div>
        {healthLoading ? (
          <div className="status-loading"><Spin /></div>
        ) : healthError ? (
          <Alert type="error" message={healthError} showIcon />
        ) : health ? (
          <div className="health-stack">
            <div className="health-row">
              <span>服务名</span>
              <strong>{health.name}</strong>
            </div>
            <div className="health-row">
              <span>版本</span>
              <strong>{health.version}</strong>
            </div>
            <div className="health-row">
              <span>环境</span>
              <Tag color="gold">{health.environment}</Tag>
            </div>
            <div className="health-row">
              <span>API 前缀</span>
              <strong>{health.api_prefix}</strong>
            </div>
            <div className="health-row">
              <span>数据库</span>
              <Tag color={health.db_enabled ? "green" : "default"}>
                {health.db_enabled ? "enabled" : "disabled"}
              </Tag>
            </div>
            <div className="health-row">
              <span>时区</span>
              <strong>{health.time_zone}</strong>
            </div>
          </div>
        ) : (
          <Empty description="暂无服务状态" />
        )}
      </Card>
    );
  }

  function renderAnalyzeCard() {
    return (
      <Card className="panel-card analyzer-card" bordered={false}>
        <div className="status-card-head">
          <div>
            <h3>BYP Analyze</h3>
            <p>输入 Excel URL 后，直接调用后端分析接口。</p>
          </div>
        </div>
        <p className="tool-input-hint">
          班易评作为工具页的一个子项独立存在，交互留在前端，分析仍然走后端。
        </p>
        <Space.Compact block>
          <Input
            size="large"
            placeholder="请输入班易评 Excel 的公开 URL"
            value={excelUrl}
            onChange={(event) => setExcelUrl(event.target.value)}
          />
          <Button type="primary" size="large" loading={analysisLoading} onClick={() => void handleAnalyze()}>
            开始分析
          </Button>
        </Space.Compact>
        {analysisError ? <Alert className="tool-alert" type="error" message={analysisError} showIcon /> : null}
        {!analysis && !analysisLoading ? (
          <div className="tool-empty">
            <Typography.Paragraph>
              输入可访问的班易评 Excel URL 后，结果会在下方直接返回班级统计和学生排行。
            </Typography.Paragraph>
          </div>
        ) : null}
      </Card>
    );
  }

  return (
    <section className="section-stack">
      {activeTab === "banyiping" ? (
        <>
          <div className="toolkit-grid">
            {renderAnalyzeCard()}
            {renderHealthCard()}
          </div>

          {analysis ? (
            <div className="analysis-grid">
              <Card className="panel-card" bordered={false}>
                <div className="result-head">
                  <h3>班级统计</h3>
                  <span>{analysis.response_at}</span>
                </div>
                <Table<ClassAnalysisItem>
                  rowKey="class_name"
                  pagination={false}
                  dataSource={analysis.class_stat}
                  columns={[
                    { title: "班级", dataIndex: "class_name" },
                    { title: "作业减分", dataIndex: "homework_deduction" },
                    { title: "日常减分", dataIndex: "daily_deduction" },
                    { title: "迟到减分", dataIndex: "late_deduction" },
                  ]}
                />
              </Card>

              <Card className="panel-card" bordered={false}>
                <div className="result-head">
                  <h3>学生排行</h3>
                  <span>Top {analysis.student_stat.length}</span>
                </div>
                <Table<StudentAnalysisItem>
                  rowKey={(record) => `${record.student_name}-${record.rank}`}
                  pagination={false}
                  dataSource={analysis.student_stat}
                  columns={[
                    { title: "排名", dataIndex: "rank", width: 88 },
                    { title: "姓名", dataIndex: "student_name" },
                    { title: "总加分", dataIndex: "total_add_score", width: 110 },
                    { title: "加分明细", dataIndex: "bonus_details" },
                  ]}
                />
              </Card>
            </div>
          ) : null}
        </>
      ) : (
        <div className="health-page-grid">
          {renderHealthCard("status-card-wide")}
          <Card className="panel-card endpoint-card" bordered={false}>
            <div className="status-card-head">
              <div>
                <h3>Endpoints</h3>
                <p>工具页里当前挂着的接口</p>
              </div>
              <Button className="ghost-action" href={`${env.apiBase}/docs`} target="_blank">
                API Docs
              </Button>
            </div>
            <div className="endpoint-stack">
              <div className="endpoint-row">
                <strong>/api/v1/system/health</strong>
                <span>服务状态</span>
              </div>
              <div className="endpoint-row">
                <strong>/api/v1/byp_analyze/</strong>
                <span>班易评分析</span>
              </div>
              <div className="endpoint-row">
                <strong>{env.apiBase}</strong>
                <span>当前 API Base</span>
              </div>
            </div>
          </Card>
        </div>
      )}
    </section>
  );
}
