import {
  Alert,
  Button,
  Card,
  Empty,
  Input,
  InputNumber,
  Select,
  Space,
  Spin,
  Switch,
  Table,
  Tag,
  message,
} from "antd";
import type { ColumnsType } from "antd/es/table";
import { useEffect, useState } from "react";

import {
  fetchServiceHealth,
  fetchOpsFeatures,
  fetchOpsLogsList,
  fetchOpsLogTail,
  fetchOpsQueryableTables,
  queryOpsTable,
  updateOpsFeature,
} from "../../api/client";
import type {
  OpsFeatureFlagRecord,
  OpsFilterOperator,
  OpsLogFileInfo,
  OpsLogTailData,
  OpsQueryableTable,
  OpsQueryableTableColumn,
  OpsTableQueryResult,
  ServiceHealthData,
} from "../../api/types";
import type { OpsTabKey } from "../../app/types";

const OPS_PAGE_PASSWORD = "1230.123";
const OPS_SESSION_KEY = "maysafe.ops.password";

type OpsPageProps = {
  activeTab: OpsTabKey;
};

function formatTime(value?: string | null) {
  if (!value) {
    return "-";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString("zh-CN", { hour12: false });
}

function initialPassword() {
  if (typeof window === "undefined") {
    return "";
  }
  return window.sessionStorage.getItem(OPS_SESSION_KEY) || "";
}

function getDefaultOrderBy(columns: OpsQueryableTableColumn[]) {
  for (const candidate of ["updated_at", "created_at", "id", "name"]) {
    if (columns.some((item) => item.name === candidate)) {
      return candidate;
    }
  }
  return columns[0]?.name || "";
}

function getDefaultFilterColumn(columns: OpsQueryableTableColumn[]) {
  return columns.find((item) => !item.hidden_by_default)?.name || columns[0]?.name || "";
}

function getDefaultOperator(column?: OpsQueryableTableColumn): OpsFilterOperator {
  if (!column) {
    return "contains";
  }
  if (column.operators.includes("contains")) {
    return "contains";
  }
  return column.operators[0] || "eq";
}

function renderCellValue(value: unknown) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  if (Array.isArray(value) || (typeof value === "object" && value !== null)) {
    return <pre className="ops-note-pre">{JSON.stringify(value, null, 2)}</pre>;
  }
  return String(value);
}

function getLatestFeatureTime(items: OpsFeatureFlagRecord[]) {
  const values = items
    .map((item) => item.updated_at)
    .filter(Boolean)
    .map((item) => new Date(item).getTime())
    .filter((value) => Number.isFinite(value));
  if (!values.length) {
    return "";
  }
  return new Date(Math.max(...values)).toISOString();
}

export function OpsPage({ activeTab }: OpsPageProps) {
  const [passwordInput, setPasswordInput] = useState(() => initialPassword());
  const [opsPassword, setOpsPassword] = useState(() => initialPassword());

  const [features, setFeatures] = useState<OpsFeatureFlagRecord[]>([]);
  const [featuresLoading, setFeaturesLoading] = useState(false);
  const [featuresError, setFeaturesError] = useState<string | null>(null);
  const [savingFeatureKey, setSavingFeatureKey] = useState("");
  const [health, setHealth] = useState<ServiceHealthData | null>(null);
  const [healthLoading, setHealthLoading] = useState(false);
  const [healthError, setHealthError] = useState<string | null>(null);

  const [logFiles, setLogFiles] = useState<OpsLogFileInfo[]>([]);
  const [selectedLog, setSelectedLog] = useState("");
  const [logKeyword, setLogKeyword] = useState("");
  const [logLines, setLogLines] = useState(200);
  const [logTail, setLogTail] = useState<OpsLogTailData | null>(null);
  const [logsLoading, setLogsLoading] = useState(false);
  const [logsError, setLogsError] = useState<string | null>(null);

  const [queryableTables, setQueryableTables] = useState<OpsQueryableTable[]>([]);
  const [selectedTable, setSelectedTable] = useState("");
  const [selectedColumn, setSelectedColumn] = useState("");
  const [selectedOperator, setSelectedOperator] = useState<OpsFilterOperator>("contains");
  const [filterValue, setFilterValue] = useState("");
  const [orderBy, setOrderBy] = useState("");
  const [orderDesc, setOrderDesc] = useState(true);
  const [tablePage, setTablePage] = useState(1);
  const [tableQuery, setTableQuery] = useState<OpsTableQueryResult | null>(null);
  const [tableLoading, setTableLoading] = useState(false);
  const [tableError, setTableError] = useState<string | null>(null);

  const unlocked = opsPassword === OPS_PAGE_PASSWORD;
  const selectedTableMeta = queryableTables.find((item) => item.name === selectedTable) || null;
  const selectedColumnMeta = selectedTableMeta?.columns.find((item) => item.name === selectedColumn);

  async function handleOpsError(error: unknown) {
    const text = error instanceof Error ? error.message : "请求失败";
    if (text.includes("运维密码错误")) {
      handleLock();
    }
    return text;
  }

  async function loadFeatures() {
    setFeaturesLoading(true);
    setFeaturesError(null);
    try {
      const response = await fetchOpsFeatures(opsPassword);
      setFeatures(response.data?.items || []);
    } catch (error) {
      setFeaturesError(await handleOpsError(error));
    } finally {
      setFeaturesLoading(false);
    }
  }

  async function loadHealth() {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const response = await fetchServiceHealth();
      setHealth(response.data ?? null);
    } catch (error) {
      setHealthError(error instanceof Error ? error.message : "服务状态获取失败");
    } finally {
      setHealthLoading(false);
    }
  }

  async function loadLogs(targetFilename?: string) {
    setLogsLoading(true);
    setLogsError(null);
    try {
      const listResponse = await fetchOpsLogsList(opsPassword);
      const files = listResponse.data?.files || [];
      setLogFiles(files);
      const nextSelected = targetFilename || selectedLog || files[0]?.name || "";
      setSelectedLog(nextSelected);
      if (!nextSelected) {
        setLogTail(null);
        return;
      }
      const tailResponse = await fetchOpsLogTail(opsPassword, {
        filename: nextSelected,
        lines: logLines,
        keyword: logKeyword || undefined,
      });
      setLogTail(tailResponse.data ?? null);
    } catch (error) {
      setLogsError(await handleOpsError(error));
    } finally {
      setLogsLoading(false);
    }
  }

  function applyTableDefaults(tables: OpsQueryableTable[], tableName?: string) {
    const resolvedTable =
      tableName
      || selectedTable
      || tables.find((item) => item.name === "item")?.name
      || tables[0]?.name
      || "";
    const meta = tables.find((item) => item.name === resolvedTable) || null;
    const nextColumn = getDefaultFilterColumn(meta?.columns || []);
    const nextColumnMeta = meta?.columns.find((item) => item.name === nextColumn);
    const nextOperator = getDefaultOperator(nextColumnMeta);
    const nextOrderBy = getDefaultOrderBy(meta?.columns || []);

    setSelectedTable(resolvedTable);
    setSelectedColumn(nextColumn);
    setSelectedOperator(nextOperator);
    setOrderBy(nextOrderBy);
    setOrderDesc(true);

    return {
      resolvedTable,
      nextColumn,
      nextOperator,
      nextOrderBy,
    };
  }

  async function loadQueryableTables(targetTable?: string, autoQuery = true) {
    setTableLoading(true);
    setTableError(null);
    try {
      const response = await fetchOpsQueryableTables(opsPassword);
      const tables = response.data?.tables || [];
      setQueryableTables(tables);
      const resolved = applyTableDefaults(tables, targetTable);
      if (autoQuery && resolved.resolvedTable) {
        await runTableQuery(1, {
          tableName: resolved.resolvedTable,
          columnName: resolved.nextColumn,
          operator: resolved.nextOperator,
          orderByValue: resolved.nextOrderBy,
          tables,
        });
      }
    } catch (error) {
      setTableError(await handleOpsError(error));
    } finally {
      setTableLoading(false);
    }
  }

  async function runTableQuery(
    page = tablePage,
    overrides?: {
      tableName?: string;
      columnName?: string;
      operator?: OpsFilterOperator;
      orderByValue?: string;
      tables?: OpsQueryableTable[];
    }
  ) {
    const tableName = overrides?.tableName || selectedTable;
    const columnName = overrides?.columnName || selectedColumn;
    const operator = overrides?.operator || selectedOperator;
    const orderByValue = overrides?.orderByValue || orderBy;
    const tables = overrides?.tables || queryableTables;
    const meta = tables.find((item) => item.name === tableName) || null;

    if (!tableName || !meta) {
      return;
    }

    setTableLoading(true);
    setTableError(null);
    try {
      const filters = [];
      if (columnName) {
        if (operator === "is_null") {
          filters.push({
            column: columnName,
            op: operator,
            value: filterValue.trim() ? filterValue.trim() : true,
          });
        } else if (filterValue.trim()) {
          filters.push({
            column: columnName,
            op: operator,
            value: filterValue.trim(),
          });
        }
      }

      const response = await queryOpsTable(opsPassword, {
        table: tableName,
        page,
        page_size: 20,
        filters,
        order_by: orderByValue || undefined,
        order_desc: orderDesc,
      });
      setTableQuery(response.data ?? null);
      setTablePage(page);
    } catch (error) {
      setTableError(await handleOpsError(error));
      setTableQuery(null);
    } finally {
      setTableLoading(false);
    }
  }

  useEffect(() => {
    if (!unlocked) {
      return;
    }
    if (activeTab === "features") {
      void loadHealth();
      void loadFeatures();
    }
    if (activeTab === "logs") {
      void loadLogs();
    }
    if (activeTab === "table") {
      void loadQueryableTables();
    }
  }, [activeTab, unlocked]);

  function handleUnlock() {
    const next = passwordInput.trim();
    if (next !== OPS_PAGE_PASSWORD) {
      message.error("密码不正确");
      return;
    }
    setOpsPassword(next);
    if (typeof window !== "undefined") {
      window.sessionStorage.setItem(OPS_SESSION_KEY, next);
    }
    message.success("运维页已解锁");
  }

  function handleLock() {
    setOpsPassword("");
    setPasswordInput("");
    setFeatures([]);
    setHealth(null);
    setHealthError(null);
    setLogFiles([]);
    setSelectedLog("");
    setLogTail(null);
    setQueryableTables([]);
    setSelectedTable("");
    setSelectedColumn("");
    setFilterValue("");
    setOrderBy("");
    setTableQuery(null);
    if (typeof window !== "undefined") {
      window.sessionStorage.removeItem(OPS_SESSION_KEY);
    }
  }

  async function handleFeatureToggle(record: OpsFeatureFlagRecord, enabled: boolean) {
    setSavingFeatureKey(record.key);
    try {
      await updateOpsFeature(opsPassword, record.key, enabled);
      setFeatures((current) =>
        current.map((item) =>
          item.key === record.key
            ? {
                ...item,
                enabled,
                updated_at: new Date().toISOString(),
              }
            : item
        )
      );
      message.success("功能开关已更新");
    } catch (error) {
      message.error(await handleOpsError(error));
    } finally {
      setSavingFeatureKey("");
    }
  }

  function renderHealthCard() {
    return (
      <Card className="panel-card ops-health-card" bordered={false}>
        <div className="status-card-head">
          <div>
            <h3>服务状态</h3>
            <p>服务、接口和数据库的当前运行状态。</p>
          </div>
          <Button onClick={() => void loadHealth()} loading={healthLoading}>
            刷新状态
          </Button>
        </div>
        {healthLoading && !health ? (
          <div className="status-loading"><Spin /></div>
        ) : healthError ? (
          <Alert type="error" message={healthError} showIcon />
        ) : health ? (
          <div className="ops-health-metrics">
            <div className="ops-health-metric ops-health-metric-primary">
              <span>服务</span>
              <strong>{health.name}</strong>
              <small>v{health.version}</small>
            </div>
            <div className="ops-health-metric">
              <span>环境</span>
              <strong>{health.environment}</strong>
            </div>
            <div className="ops-health-metric">
              <span>API</span>
              <strong>{health.api_prefix}</strong>
            </div>
            <div className="ops-health-metric">
              <span>数据库</span>
              <strong>{health.db_enabled ? "enabled" : "disabled"}</strong>
              <Tag color={health.db_enabled ? "green" : "default"}>
                {health.db_enabled ? "online" : "off"}
              </Tag>
            </div>
            <div className="ops-health-metric">
              <span>时区</span>
              <strong>{health.time_zone}</strong>
            </div>
            <div className="ops-health-metric">
              <span>响应时间</span>
              <strong>{formatTime(health.response_at)}</strong>
            </div>
          </div>
        ) : (
          <Empty description="暂无服务状态" />
        )}
      </Card>
    );
  }

  function renderConsoleSummaryCard() {
    const enabledCount = features.filter((item) => item.enabled).length;
    const groups = Array.from(new Set(features.map((item) => item.group))).filter(Boolean);
    const latestUpdated = getLatestFeatureTime(features);

    return (
      <Card className="panel-card ops-console-summary-card" bordered={false}>
        <div className="status-card-head">
          <div>
            <h3>控制台概览</h3>
            <p>当前开关数量和最新变更时间。</p>
          </div>
        </div>
        <div className="ops-console-summary-grid">
          <div className="ops-console-summary-item">
            <span>功能总数</span>
            <strong>{features.length}</strong>
          </div>
          <div className="ops-console-summary-item">
            <span>已开启</span>
            <strong>{enabledCount}</strong>
          </div>
          <div className="ops-console-summary-item">
            <span>分组</span>
            <strong>{groups.length}</strong>
          </div>
          <div className="ops-console-summary-item">
            <span>最近更新</span>
            <strong>{latestUpdated ? formatTime(latestUpdated) : "-"}</strong>
          </div>
        </div>
        {groups.length ? (
          <div className="ops-feature-meta">
            {groups.map((group) => (
              <span key={group} className="ops-feature-meta-pill">
                <span>group</span>
                <strong>{group}</strong>
              </span>
            ))}
          </div>
        ) : null}
      </Card>
    );
  }

  function renderConsole() {
    const orderedFeatures = [...features].sort((left, right) => {
      const groupCompare = left.group.localeCompare(right.group);
      if (groupCompare !== 0) {
        return groupCompare;
      }
      return left.label.localeCompare(right.label);
    });

    return (
      <div className="section-stack ops-console-shell">
        <div className="ops-console-top">
          {renderHealthCard()}
          {renderConsoleSummaryCard()}
        </div>
        {featuresError ? <Alert type="error" message={featuresError} showIcon /> : null}
        {featuresLoading ? (
          <div className="status-loading"><Spin /></div>
        ) : (
          <div className="ops-feature-grid">
            {orderedFeatures.map((item) => (
              <Card key={item.key} className="panel-card ops-feature-card" bordered={false}>
                <div className="ops-feature-top">
                  <div>
                    <div className="ops-feature-headline">
                      <h3>{item.label}</h3>
                      <Tag>{item.group}</Tag>
                    </div>
                    <p>{item.description}</p>
                  </div>
                  <Switch
                    checked={item.enabled}
                    loading={savingFeatureKey === item.key}
                    onChange={(checked) => void handleFeatureToggle(item, checked)}
                  />
                </div>
                <div className="ops-feature-meta">
                  <span className="ops-feature-meta-pill">
                    <span>key</span>
                    <strong>{item.key}</strong>
                  </span>
                  <span className="ops-feature-meta-pill">
                    <span>updated</span>
                    <strong>{formatTime(item.updated_at)}</strong>
                  </span>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    );
  }

  function renderLogs() {
    return (
      <div className="section-stack">
        {logsError ? <Alert type="error" message={logsError} showIcon /> : null}
        <Card className="panel-card" bordered={false}>
          <div className="ops-toolbar-row">
            <Select
              className="ops-flex-item"
              value={selectedLog || undefined}
              placeholder="选择日志文件"
              options={logFiles.map((item) => ({ label: item.name, value: item.name }))}
              onChange={(value) => {
                const next = String(value || "");
                setSelectedLog(next);
                void loadLogs(next);
              }}
            />
            <Input
              className="ops-flex-item"
              value={logKeyword}
              placeholder="关键字过滤"
              onChange={(event) => setLogKeyword(event.target.value)}
              onPressEnter={() => void loadLogs(selectedLog)}
            />
            <InputNumber min={20} max={2000} value={logLines} onChange={(value) => setLogLines(Number(value || 200))} />
            <Button onClick={() => void loadLogs(selectedLog)} loading={logsLoading}>刷新</Button>
          </div>
          <div className="log-toolbar">
            <span className="status">
              {logTail
                ? `${logTail.file} · 总行数 ${logTail.total_lines} · 命中 ${logTail.matched_lines}`
                : "暂无日志内容"}
            </span>
          </div>
          <div className="log-console">
            {logsLoading ? <Spin /> : <pre>{logTail?.lines?.length ? logTail.lines.join("\n") : "(暂无内容)"}</pre>}
          </div>
        </Card>
      </div>
    );
  }

  function renderTableQuery() {
    const tableColumns: ColumnsType<Record<string, unknown>> = (tableQuery?.columns || []).map((column) => ({
      title: column,
      dataIndex: column,
      key: column,
      render: (value: unknown) => renderCellValue(value),
    }));

    return (
      <div className="section-stack">
        {tableError ? <Alert type="error" message={tableError} showIcon /> : null}
        <Card className="panel-card" bordered={false}>
          <div className="ops-toolbar-row wrap">
            <Select
              className="ops-flex-item"
              value={selectedTable || undefined}
              placeholder="选择数据表"
              options={queryableTables.map((item) => ({ label: item.name, value: item.name }))}
              onChange={(value) => {
                const nextTable = String(value || "");
                const nextMeta = queryableTables.find((item) => item.name === nextTable) || null;
                const nextColumn = getDefaultFilterColumn(nextMeta?.columns || []);
                const nextColumnMeta = nextMeta?.columns.find((item) => item.name === nextColumn);
                const nextOperator = getDefaultOperator(nextColumnMeta);
                const nextOrderBy = getDefaultOrderBy(nextMeta?.columns || []);
                setSelectedTable(nextTable);
                setSelectedColumn(nextColumn);
                setSelectedOperator(nextOperator);
                setOrderBy(nextOrderBy);
                setFilterValue("");
                void runTableQuery(1, {
                  tableName: nextTable,
                  columnName: nextColumn,
                  operator: nextOperator,
                  orderByValue: nextOrderBy,
                });
              }}
            />
            <Select
              className="ops-flex-item"
              value={selectedColumn || undefined}
              placeholder="筛选字段"
              options={(selectedTableMeta?.columns || []).map((item) => ({
                label: `${item.name} (${item.type})`,
                value: item.name,
              }))}
              onChange={(value) => {
                const nextColumn = String(value || "");
                const nextMeta = selectedTableMeta?.columns.find((item) => item.name === nextColumn);
                setSelectedColumn(nextColumn);
                setSelectedOperator(getDefaultOperator(nextMeta));
              }}
            />
            <Select
              className="ops-flex-item"
              value={selectedOperator}
              placeholder="操作符"
              options={(selectedColumnMeta?.operators || ["eq"]).map((item) => ({
                label: item,
                value: item,
              }))}
              onChange={(value) => setSelectedOperator(value as OpsFilterOperator)}
            />
            <Input
              className="ops-flex-item"
              value={filterValue}
              placeholder={selectedOperator === "is_null" ? "留空表示 true，可填 false" : "筛选值"}
              onChange={(event) => setFilterValue(event.target.value)}
              onPressEnter={() => void runTableQuery(1)}
            />
            <Select
              className="ops-flex-item"
              value={orderBy || undefined}
              placeholder="排序字段"
              options={(selectedTableMeta?.columns || []).map((item) => ({
                label: item.name,
                value: item.name,
              }))}
              onChange={(value) => setOrderBy(String(value || ""))}
            />
            <Select
              value={orderDesc ? "desc" : "asc"}
              options={[
                { label: "倒序", value: "desc" },
                { label: "正序", value: "asc" },
              ]}
              onChange={(value) => setOrderDesc(String(value) === "desc")}
            />
            <Button type="primary" onClick={() => void runTableQuery(1)} loading={tableLoading}>
              查询
            </Button>
          </div>

          {selectedTableMeta ? (
            <div className="ops-query-meta">
              <span>当前表：{selectedTableMeta.name}</span>
              <span>字段数：{selectedTableMeta.columns.length}</span>
            </div>
          ) : null}

          <Table<Record<string, unknown>>
            rowKey={(record, index) => String(record.id || `${tableQuery?.table || "row"}-${index}`)}
            loading={tableLoading}
            dataSource={tableQuery?.rows || []}
            columns={tableColumns}
            scroll={{ x: true }}
            pagination={{
              current: tableQuery?.page || tablePage,
              pageSize: tableQuery?.page_size || 20,
              total: tableQuery?.total_count || 0,
              onChange: (page) => {
                void runTableQuery(page);
              },
            }}
            locale={{ emptyText: tableLoading ? "查询中..." : "暂无结果" }}
          />
        </Card>
      </div>
    );
  }

  if (!unlocked) {
    return (
      <div className="ops-auth-shell">
        <Card className="panel-card ops-auth-card" bordered={false}>
          <span className="section-chip">Ops</span>
          <h2>运维控制台</h2>
          <Space.Compact block>
            <Input.Password
              size="large"
              placeholder="请输入运维密码"
              value={passwordInput}
              onChange={(event) => setPasswordInput(event.target.value)}
              onPressEnter={handleUnlock}
            />
            <Button type="primary" size="large" onClick={handleUnlock}>
              进入
            </Button>
          </Space.Compact>
        </Card>
      </div>
    );
  }

  return (
    <div className="page-stack">
      <div className="ops-toolbar actions">
        <Space>
          <Button
            onClick={() => {
              if (activeTab === "features") {
                void loadHealth();
                void loadFeatures();
              }
              if (activeTab === "logs") {
                void loadLogs(selectedLog);
              }
              if (activeTab === "table") {
                void loadQueryableTables(selectedTable);
              }
            }}
          >
            刷新
          </Button>
          <Button onClick={handleLock}>锁定</Button>
        </Space>
      </div>

      {activeTab === "features" ? renderConsole() : null}
      {activeTab === "logs" ? renderLogs() : null}
      {activeTab === "table" ? renderTableQuery() : null}
    </div>
  );
}
