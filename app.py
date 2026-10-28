import os
import io
import base64
import numpy as np

# Gunakan backend Agg agar Matplotlib tidak membuka GUI window saat dijalankan di server
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, request

app = Flask(__name__)

# ==========================================================
# HELPER: Konversi Matplotlib Figure ke Base64 String
# ==========================================================
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def clean_zero(val, threshold=1e-9):
    """Menghilangkan tampilan -0.0000 agar menjadi 0.0000"""
    return 0.0 if abs(val) < threshold else val


# ==========================================================
# 1. HALAMAN BERANDA (HOME)
# ==========================================================
@app.route('/')
def index():
    return render_template('index.html')


# ==========================================================
# 2. HALAMAN METODE TABEL
# Fungsi: f(x) = x^2 + 3*e^x
# ==========================================================
def f_tabel(x):
    return (x ** 2) + 3.0 * np.exp(x)

def generate_tabel_chart(trials_data):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    
    # Plot kurva fungsi utama
    x_plot = np.linspace(-3.2, 0.5, 400)
    y_plot = f_tabel(x_plot)
    ax.plot(x_plot, y_plot, color='#2563eb', lw=2.5, label=r'$f(x) = x^2 + 3e^x$')
    
    # Garis y = 0
    ax.axhline(0, color='#dc2626', linestyle='--', lw=1.5, alpha=0.8, label=r'Garis $y = 0$ (Target Akar)')
    
    # Titik minimum f(x) di sekitar x = -0.7268 (f(x) ~ 1.9786)
    x_min = -0.7268
    y_min = f_tabel(x_min)
    ax.scatter([x_min], [y_min], color='#d97706', s=60, zorder=5, label=f'Titik Minimum f({x_min:.3f}) = {y_min:.3f}')
    ax.annotate(f'Min: ({x_min:.3f}, {y_min:.3f})', 
                xy=(x_min, y_min), 
                xytext=(x_min + 0.3, y_min + 1.2),
                arrowprops=dict(facecolor='#d97706', shrink=0.08, width=1, headwidth=6),
                fontsize=9, fontweight='bold', color='#92400e')

    # Visualisasi rentang percobaan ke-1
    ax.axvspan(-3, 0, color='#3b82f6', alpha=0.08, label='Area Percobaan 1 [-3, 0]')
    
    ax.set_title('Grafik Fungsi Metode Tabel: f(x) = x² + 3eˣ', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Nilai x', fontsize=10)
    ax.set_ylabel('Nilai f(x)', fontsize=10)
    ax.set_ylim(-0.8, max(y_plot) * 1.05)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    
    return fig_to_base64(fig)

@app.route('/tabel', methods=['GET', 'POST'])
def tabel():
    # Pengaturan default 4 percobaan
    default_trials = [
        {'id': 1, 'nama': 'Percobaan 1', 'bawah': -3.0, 'atas': 0.0, 'n': 10},
        {'id': 2, 'nama': 'Percobaan 2', 'bawah': -0.9, 'atas': -0.6, 'n': 10},
        {'id': 3, 'nama': 'Percobaan 3', 'bawah': -0.75, 'atas': -0.72, 'n': 10},
        {'id': 4, 'nama': 'Percobaan 4', 'bawah': -0.729, 'atas': -0.726, 'n': 10},
    ]
    
    trials_data = []
    
    for i in range(1, 5):
        try:
            bawah = float(request.form.get(f'bawah_{i}', default_trials[i-1]['bawah']))
            atas = float(request.form.get(f'atas_{i}', default_trials[i-1]['atas']))
            n = int(request.form.get(f'n_{i}', default_trials[i-1]['n']))
            if n <= 0:
                n = 10
        except (ValueError, TypeError):
            bawah = default_trials[i-1]['bawah']
            atas = default_trials[i-1]['atas']
            n = default_trials[i-1]['n']
            
        h = (atas - bawah) / n if n != 0 else 0
        
        # Hitung tiap baris tabel i=0 sampai n
        rows = []
        min_row_idx = 0
        min_val = float('inf')
        
        for step in range(n + 1):
            xi = bawah + (step * h)
            fxi = f_tabel(xi)
            if fxi < min_val:
                min_val = fxi
                min_row_idx = step
                
            rows.append({
                'i': step,
                'xi': f"{xi:.6f}",
                'fxi': f"{fxi:.6f}",
                'fxi_raw': fxi
            })
            
        trials_data.append({
            'id': i,
            'nama': f"Percobaan {i}",
            'bawah': bawah,
            'atas': atas,
            'n': n,
            'h': f"{h:.6f}",
            'rows': rows,
            'min_row_idx': min_row_idx,
            'min_val': min_val
        })
        
    chart_base64 = generate_tabel_chart(trials_data)
    
    # Kesimpulan dinamis:
    kesimpulan = (
        "Berdasarkan hasil pemindaian 4 percobaan tabel nilai di atas serta visualisasi kurva grafik, "
        "nilai f(x) selalu positif (f(x) > 0) dan mencapai nilai minimum di sekitar x ≈ -0.726 dengan f(x) ≈ 1.9786. "
        "Karena kurva f(x) tidak pernah menyentuh maupun memotong sumbu x (f(x) = 0), maka persamaan f(x) = x² + 3eˣ "
        "tidak memiliki akar real."
    )
    
    return render_template('tabel.html', 
                           trials=trials_data, 
                           chart_base64=chart_base64, 
                           kesimpulan=kesimpulan)


# ==========================================================
# 3. HALAMAN METODE BISEKSI
# Fungsi: f(x) = 2^x - 2 - x^2
# ==========================================================
def f_biseksi(x):
    return (2.0 ** x) - 2.0 - (x ** 2)

def generate_biseksi_chart(xi_init, xu_init, root_val, rows):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    
    x_min = min(xi_init, 2.5) - 0.5
    x_max = max(xu_init, 5.5) + 0.5
    x_plot = np.linspace(x_min, x_max, 400)
    y_plot = f_biseksi(x_plot)
    
    ax.plot(x_plot, y_plot, color='#2563eb', lw=2.5, label=r'$f(x) = 2^x - 2 - x^2$')
    ax.axhline(0, color='#64748b', linestyle='--', lw=1.2, alpha=0.8, label=r'$y = 0$')
    
    # Batas awal
    ax.axvline(xi_init, color='#10b981', linestyle=':', lw=1.5, label=f'Batas Awal xi = {xi_init}')
    ax.axvline(xu_init, color='#f59e0b', linestyle=':', lw=1.5, label=f'Batas Awal xu = {xu_init}')
    
    # Titik akar yang didapat
    if root_val is not None:
        f_root = f_biseksi(root_val)
        ax.scatter([root_val], [f_root], color='#dc2626', s=90, zorder=6, label=f'Akar x ≈ {root_val:.4f}')
        ax.annotate(f'Akar: x={root_val:.4f}\nf(x)={f_root:.4f}', 
                    xy=(root_val, f_root), 
                    xytext=(root_val - 1.2, f_root + 3.0),
                    arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.5, headwidth=6),
                    fontsize=9, fontweight='bold', color='#991b1b',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee2e2', edgecolor='#fca5a5', alpha=0.9))
                    
    ax.set_title('Grafik Metode Biseksi: f(x) = 2ˣ - 2 - x²', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Nilai x', fontsize=10)
    ax.set_ylabel('Nilai f(x)', fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', frameon=True, fontsize=9)
    
    return fig_to_base64(fig)

@app.route('/biseksi', methods=['GET', 'POST'])
def biseksi():
    # Default values
    default_xi = 3.0
    default_xu = 5.0
    default_tol = 0.5 # Persen (0.5%)
    max_iter = 50
    
    try:
        xi_input = float(request.form.get('xi', default_xi))
        xu_input = float(request.form.get('xu', default_xu))
        tol_input = float(request.form.get('tol', default_tol))
    except (ValueError, TypeError):
        xi_input = default_xi
        xu_input = default_xu
        tol_input = default_tol
        
    xi = xi_input
    xu = xu_input
    tol = tol_input
    
    rows = []
    r_old = None
    converged = False
    found_root = None
    final_iter = 0
    final_error = 0.0
    final_fr = 0.0
    warning_message = None
    
    # Validasi tebakan awal teorema Bolzano
    f_xi_init = f_biseksi(xi)
    f_xu_init = f_biseksi(xu)
    if f_xi_init * f_xu_init > 0:
        warning_message = f"Perhatian: f(xi) = {f_xi_init:.4f} dan f(xu) = {f_xu_init:.4f} memiliki tanda yang sama (f(xi) * f(xu) > 0). Akar mungkin tidak dijamin berada di selang ini."
        
    for i in range(1, max_iter + 1):
        r = (xi + xu) / 2.0
        f_xi = f_biseksi(xi)
        f_xu = f_biseksi(xu)
        f_r = f_biseksi(r)
        
        # Hitung error relatif dalam persen
        if r_old is not None:
            err = abs((r - r_old) / r) * 100.0 if r != 0 else abs(r - r_old) * 100.0
        else:
            err = None
            
        rows.append({
            'i': i,
            'xi': f"{clean_zero(xi):.4f}",
            'xu': f"{clean_zero(xu):.4f}",
            'r': f"{clean_zero(r):.4f}",
            'f_xi': f"{clean_zero(f_xi):.4f}",
            'f_xu': f"{clean_zero(f_xu):.4f}",
            'f_r': f"{clean_zero(f_r):.4f}",
            'error': f"{err:.4f}%" if err is not None else "-"
        })
        
        if err is not None and err <= tol:
            converged = True
            found_root = r
            final_iter = i
            final_error = err
            final_fr = f_r
            break
            
        if abs(f_r) < 1e-12:
            converged = True
            found_root = r
            final_iter = i
            final_error = err if err is not None else 0.0
            final_fr = f_r
            break
            
        # Pembaruan batas
        if f_xi * f_r < 0:
            xu = r
        else:
            xi = r
            
        r_old = r
        
    if not converged:
        found_root = r
        final_iter = len(rows)
        final_error = err if err is not None else 0.0
        final_fr = f_r
        
    # Buat kalimat kesimpulan dinamis
    if converged:
        kesimpulan = (
            f"Akar ditemukan pada iterasi ke-{final_iter} dengan nilai hampiran akar "
            f"x ≈ {clean_zero(found_root):.4f}, nilai f(x) = {clean_zero(final_fr):.4f}, "
            f"dan galat relatif sebesar {final_error:.4f}% (telah memenuhi toleransi ≤ {tol}%)."
        )
    else:
        kesimpulan = (
            f"Iterasi berhenti pada batas maksimal ({max_iter} iterasi) dengan nilai hampiran akar "
            f"x ≈ {clean_zero(found_root):.4f}, f(x) = {clean_zero(final_fr):.4f}, galat = {final_error:.4f}% "
            f"(belum mencapai target toleransi {tol}%)."
        )
        
    chart_base64 = generate_biseksi_chart(xi_input, xu_input, found_root, rows)
    
    return render_template('biseksi.html',
                           xi=xi_input,
                           xu=xu_input,
                           tol=tol_input,
                           rows=rows,
                           final_iter=final_iter,
                           found_root=clean_zero(found_root),
                           kesimpulan=kesimpulan,
                           converged=converged,
                           warning_message=warning_message,
                           chart_base64=chart_base64)


# ==========================================================
# 4. HALAMAN NEWTON-RAPHSON & SECANT
# Fungsi: f(x) = x^2 + e^(-2x) * sin(x)
# ==========================================================
def f_ns(x):
    return (x ** 2) + np.exp(-2.0 * x) * np.sin(x)

def df_ns(x):
    return 2.0 * x - 2.0 * np.exp(-2.0 * x) * np.sin(x) + np.exp(-2.0 * x) * np.cos(x)

def generate_ns_chart(x0_newton, root_newton, xr_secant, root_secant):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    
    # Subplot 1: Tinjauan Luas (f(x) di rentang lebar [-1, 10])
    x_broad = np.linspace(-0.5, 10.5, 400)
    y_broad = f_ns(x_broad)
    ax1.plot(x_broad, y_broad, color='#2563eb', lw=2, label=r'$f(x) = x^2 + e^{-2x}\sin(x)$')
    ax1.axhline(0, color='#dc2626', linestyle='--', alpha=0.7, label=r'$y = 0$')
    ax1.scatter([xr_secant], [f_ns(xr_secant)], color='#ea580c', s=50, label=f'Titik Awal Secant xr = {xr_secant}')
    ax1.scatter([root_secant], [f_ns(root_secant)], color='#16a34a', s=70, zorder=5, label=f'Akar x ≈ {clean_zero(root_secant):.4f}')
    ax1.set_title('Tinjauan Luas (Domain Global Secant)', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Nilai x', fontsize=9)
    ax1.set_ylabel('f(x)', fontsize=9)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', fontsize=8)

    # Subplot 2: Zoom di sekitar Akar x = 0 [-1, 1.5]
    x_zoom = np.linspace(-0.6, 1.2, 400)
    y_zoom = f_ns(x_zoom)
    ax2.plot(x_zoom, y_zoom, color='#2563eb', lw=2.5, label=r'$f(x)$')
    ax2.axhline(0, color='#dc2626', linestyle='--', alpha=0.7, label=r'$y = 0$')
    ax2.scatter([x0_newton], [f_ns(x0_newton)], color='#d97706', s=60, label=f'x0 Newton = {x0_newton}')
    ax2.scatter([root_newton], [f_ns(root_newton)], color='#16a34a', s=90, zorder=6, label=f'Akar x ≈ {clean_zero(root_newton):.4f}')
    ax2.annotate(f'Akar Real:\nx = {clean_zero(root_newton):.4f}', 
                 xy=(root_newton, f_ns(root_newton)), 
                 xytext=(root_newton + 0.25, f_ns(root_newton) + 0.35),
                 arrowprops=dict(facecolor='#16a34a', shrink=0.08, width=1.5, headwidth=6),
                 fontsize=9, fontweight='bold', color='#15803d',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#dcfce7', edgecolor='#86efac'))
    ax2.set_title('Detail di Sekitar Titik Konvergensi x = 0', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Nilai x', fontsize=9)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', fontsize=8)
    
    plt.tight_layout()
    return fig_to_base64(fig)

@app.route('/newton-secant', methods=['GET', 'POST'])
def newton_secant():
    # Parameter default Newton-Raphson
    default_x0 = 0.5
    default_tol_newton = 0.0001
    max_iter_newton = 30
    
    # Parameter default Secant
    default_xr_min1 = 0.5
    default_xr = 10.0
    default_tol_secant = 0.0001
    max_iter_secant = 30
    
    try:
        x0 = float(request.form.get('x0', default_x0))
        tol_newton = float(request.form.get('tol_newton', default_tol_newton))
    except (ValueError, TypeError):
        x0 = default_x0
        tol_newton = default_tol_newton

    try:
        xr_min1 = float(request.form.get('xr_min1', default_xr_min1))
        xr = float(request.form.get('xr', default_xr))
        tol_secant = float(request.form.get('tol_secant', default_tol_secant))
    except (ValueError, TypeError):
        xr_min1 = default_xr_min1
        xr = default_xr
        tol_secant = default_tol_secant

    # -----------------------------
    # Perhitungan Newton-Raphson
    # Rumus: x_{i+1} = x_i - f(x_i)/f'(x_i)
    # Tabel: i, xi, f(xi), f'(xi), error
    # -----------------------------
    rows_newton = []
    curr_x = x0
    root_newton = curr_x
    iter_newton = 0
    converged_newton = False
    
    for i in range(1, max_iter_newton + 1):
        f_val = f_ns(curr_x)
        df_val = df_ns(curr_x)
        
        if abs(df_val) < 1e-14:
            # Hindari pembagian dengan nol jika turunan nol
            err = 0.0
            x_next = curr_x
            rows_newton.append({
                'i': i,
                'xi': f"{clean_zero(curr_x):.4f}",
                'fxi': f"{clean_zero(f_val):.4f}",
                'dfxi': f"{clean_zero(df_val):.4f}",
                'error': f"{err:.4f}",
                'x_next': f"{clean_zero(x_next):.4f}"
            })
            root_newton = curr_x
            iter_newton = i
            break
            
        x_next = curr_x - (f_val / df_val)
        err = abs(x_next - curr_x)
        
        rows_newton.append({
            'i': i,
            'xi': f"{clean_zero(curr_x):.4f}",
            'fxi': f"{clean_zero(f_val):.4f}",
            'dfxi': f"{clean_zero(df_val):.4f}",
            'error': f"{err:.4f}",
            'x_next': f"{clean_zero(x_next):.4f}"
        })
        
        if err <= tol_newton or abs(f_val) <= 1e-7:
            converged_newton = True
            root_newton = x_next
            iter_newton = i
            break
            
        curr_x = x_next
        root_newton = curr_x
        iter_newton = i
        
    f_root_newton = f_ns(root_newton)
    kesimpulan_newton = (
        f"Metode Newton-Raphson: Akar ditemukan pada iterasi ke-{iter_newton} dengan nilai hampiran "
        f"akar x ≈ {clean_zero(root_newton):.4f}, f(x) = {clean_zero(f_root_newton):.4f}, "
        f"dan nilai galat {rows_newton[-1]['error']} (memenuhi toleransi ≤ {tol_newton})."
    )

    # -----------------------------
    # Perhitungan Secant
    # Rumus: x_{r+1} = x_r - f(x_r)*(x_r - x_{r-1}) / (f(x_r) - f(x_{r-1}))
    # Tabel: i, xr, f(xr), error (dengan informasi xr-1)
    # -----------------------------
    rows_secant = []
    p_prev = xr_min1
    p_curr = xr
    root_secant = p_curr
    iter_secant = 0
    converged_secant = False
    
    for i in range(1, max_iter_secant + 1):
        f_prev = f_ns(p_prev)
        f_curr = f_ns(p_curr)
        denom = f_curr - f_prev
        
        if abs(denom) < 1e-14:
            p_next = p_curr
            err = 0.0
            rows_secant.append({
                'i': i,
                'xr_prev': f"{clean_zero(p_prev):.4f}",
                'xr': f"{clean_zero(p_curr):.4f}",
                'fxr': f"{clean_zero(f_curr):.4f}",
                'error': f"{err:.4f}",
                'xr_next': f"{clean_zero(p_next):.4f}"
            })
            root_secant = p_curr
            iter_secant = i
            break
            
        p_next = p_curr - f_curr * (p_curr - p_prev) / denom
        err = abs(p_next - p_curr)
        
        rows_secant.append({
            'i': i,
            'xr_prev': f"{clean_zero(p_prev):.4f}",
            'xr': f"{clean_zero(p_curr):.4f}",
            'fxr': f"{clean_zero(f_curr):.4f}",
            'error': f"{err:.4f}",
            'xr_next': f"{clean_zero(p_next):.4f}"
        })
        
        if err <= tol_secant or abs(f_curr) <= 1e-7:
            converged_secant = True
            root_secant = p_next
            iter_secant = i
            break
            
        p_prev = p_curr
        p_curr = p_next
        root_secant = p_curr
        iter_secant = i
        
    f_root_secant = f_ns(root_secant)
    kesimpulan_secant = (
        f"Metode Secant: Akar ditemukan pada iterasi ke-{iter_secant} dengan nilai hampiran "
        f"akar x ≈ {clean_zero(root_secant):.4f}, f(x) = {clean_zero(f_root_secant):.4f}, "
        f"dan nilai galat {rows_secant[-1]['error']} (memenuhi toleransi ≤ {tol_secant})."
    )

    chart_base64 = generate_ns_chart(x0, root_newton, xr, root_secant)
    
    return render_template('newton_secant.html',
                           x0=x0,
                           tol_newton=tol_newton,
                           rows_newton=rows_newton,
                           kesimpulan_newton=kesimpulan_newton,
                           root_newton=clean_zero(root_newton),
                           xr_min1=xr_min1,
                           xr=xr,
                           tol_secant=tol_secant,
                           rows_secant=rows_secant,
                           kesimpulan_secant=kesimpulan_secant,
                           root_secant=clean_zero(root_secant),
                           chart_base64=chart_base64)


if __name__ == '__main__':
    # Jalankan server Flask di port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
