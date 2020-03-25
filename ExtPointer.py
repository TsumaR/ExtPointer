#coding utf-8
import extractpoint
import cv2
import os,sys
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


# 参照ボタンの作成。二つ。
def ask_before():
    path = filedialog.askopenfilename()
    before_path.set(path)
def ask_after():
    paths = filedialog.askopenfilename()
    after_path.set(paths)
def ask_output():
    paths = filedialog.askdirectory()
    outdir_path.set(paths)

def app():
    # 実行ボタンの動作
    before_file = before_path.get()
    after_file = after_path.get()
    out_dir = outdir_path.get()
    dist_val = int(EditBox.get())
    # output tsv file
    smpl_pos = extractpoint.detect_sampling_point(after_file, dist_val)
    smpl_pos.to_csv('%s/%s_sampling_point.tsv' % (out_dir, os.path.basename(after_file)), sep='\t')
    # output sampling point fig
    after_point_img = extractpoint.marker_sampling_point(after_file, smpl_pos)
    before_point_img = extractpoint.marker_sampling_point(before_file, smpl_pos)
    cv2.imwrite('%s/%s_sampling_point.jpg' % (out_dir, os.path.basename(after_file)), after_point_img)
    cv2.imwrite('%s/%s_sampling_point.jpg' % (out_dir, os.path.basename(before_file)), before_point_img)
    messagebox.showinfo("完了", "完了しました。")


if __name__ == '__main__':
    main_win = tkinter.Tk()
    main_win.title('File shrink')

    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=5)

    #before
    before_label = ttk.Label(main_frm, text="before>>")
    before_path = tkinter.StringVar()
    before_box = ttk.Entry(main_frm, width = 30, textvariable=before_path)
    before_btn = ttk.Button(main_frm, text="参照", command=ask_before)

    before_label.grid(column=0, row=0, pady=10)
    before_box.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
    before_btn.grid(column=2, row=0)

    #after
    after_label = ttk.Label(main_frm, text="after>>")
    after_path = tkinter.StringVar()
    after_box = ttk.Entry(main_frm, width = 30, textvariable=after_path)
    after_btn = ttk.Button(main_frm, text="参照", command=ask_after)

    after_label.grid(column=0, row=1, pady=10)
    after_box.grid(column=1, row=1, sticky=tkinter.EW, padx=5)
    after_btn.grid(column=2, row=1)

    #output
    output_label = ttk.Label(main_frm, text="output>>")
    outdir_path = tkinter.StringVar()
    output_box = ttk.Entry(main_frm, width = 30, textvariable=outdir_path)
    output_btn = ttk.Button(main_frm, text="参照", command=ask_output)

    output_label.grid(column=0, row=2, pady=10)
    output_box.grid(column=1, row=2, sticky=tkinter.EW, padx=5)
    output_btn.grid(column=2, row=2)

    #distance value
    EditBox_label = ttk.Label(main_frm, text="点の間の距離")
    EditBox = ttk.Entry(main_frm, width=5)

    EditBox_label.grid(column=0, row=3)
    EditBox.grid(column=1, row=3, sticky=tkinter.EW, padx=5)

    #file type
    #Extension_box

    #shrink
    app_btn = ttk.Button(main_frm, text="実行", command=app)
    app_btn.grid(column=1, row=4)

    #row.columnconfigure(0, weight=1)
    #row.rowconfigure(0, weight=1)
    #row.columnconfigure(1, weight=1)

    main_win.columnconfigure(0, weight=1)
    main_win.rowconfigure(0, weight=1)
    main_frm.columnconfigure(1, weight=1)

    main_win.mainloop()
