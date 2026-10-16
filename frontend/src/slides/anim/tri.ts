// Общее для сцен про треугольник Паскаля: биномиальные коэффициенты и раскладка клеток.
export const binom = (n: number, k: number) => {
  let r = 1;
  for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i;
  return Math.round(r);
};
// центр клетки строки r, номера c в треугольнике с шагом dx, dy
export const triPos = (r: number, c: number, dx = 36, dy = 22, cx = 180, y0 = 20) => [
  cx + (c - r / 2) * dx,
  y0 + r * dy,
];
