/* Итог проверки в стиле приложения: компактная плашка — значок, заголовок, пояснение, кнопка «дальше». */
export default function ResultAlert({
  ok = true,
  title,
  children,
  onNext,
  nextLabel,
}) {
  const label = (nextLabel || "Следующее").replace(/\s*→\s*$/, "");
  return (
    <div className={`lab-alert ${ok ? "ok" : "bad"}`} role="status">
      <span className="lab-alert-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24">
          {ok ? (
            <path d="M20 6 9 17l-5-5" />
          ) : (
            <path d="M18 6 6 18M6 6l12 12" />
          )}
        </svg>
      </span>
      <div className="lab-alert-body">
        <p className="lab-alert-title">{title}</p>
        {children && <p className="lab-alert-text">{children}</p>}
      </div>
      {onNext && (
        <button type="button" className="lab-alert-next" onClick={onNext}>
          {label}
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      )}
    </div>
  );
}
