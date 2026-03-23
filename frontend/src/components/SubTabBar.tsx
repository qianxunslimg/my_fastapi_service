type SubTabItem = {
  key: string;
  label: string;
};

type SubTabBarProps = {
  items: SubTabItem[];
  activeKey: string;
  onChange: (key: string) => void;
  className?: string;
};

export function SubTabBar({ items, activeKey, onChange, className }: SubTabBarProps) {
  const classes = ["section-subtab-bar", className].filter(Boolean).join(" ");

  return (
    <div className={classes}>
      {items.map((item) => (
        <button
          key={item.key}
          type="button"
          className={`section-subtab-btn${item.key === activeKey ? " is-active" : ""}`}
          onClick={() => onChange(item.key)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
