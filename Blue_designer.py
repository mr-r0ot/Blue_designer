import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

# تنظیمات اولیه
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class AdvancedAppDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced App Designer")
        self.root.geometry("1200x750")
        self.root.configure(bg="#ececec")

        # حالت شبیه‌سازی: Mobile یا Web
        self.simulation_mode = ctk.StringVar(value="Mobile")

        # المان انتخاب‌شده (container انتخاب شده)
        self.selected_container = None

        # لیست المان‌های ایجاد شده (هر المطلب در یک container قرار می‌گیرد)
        self.elements = []  # هر مورد یک دیکشنری با کلیدهای: container، type، custom_code (اختیاری)

        # ایجاد بخش‌های اصلی رابط کاربری
        self.create_top_menu()
        self.create_tool_panel()
        self.create_simulation_area()
        self.create_properties_panel()
        self.create_bottom_panel()

    # --------------- بخش منو و نوار ابزار ---------------
    def create_top_menu(self):
        """ایجاد منوی بالایی شامل عنوان و تغییر مد شبیه‌سازی"""
        self.top_frame = ctk.CTkFrame(self.root, width=1200, height=50, fg_color="#d0d0d0")
        self.top_frame.pack(side="top", fill="x", padx=10, pady=5)

        title_label = ctk.CTkLabel(self.top_frame, text="Advanced App Designer", font=("Arial", 18, "bold"))
        title_label.pack(side="left", padx=10)

        mode_label = ctk.CTkLabel(self.top_frame, text="Simulation Mode:", font=("Arial", 14))
        mode_label.pack(side="left", padx=(50, 5))

        mode_option = ctk.CTkOptionMenu(
            self.top_frame,
            values=["Mobile", "Web"],
            variable=self.simulation_mode,
            command=self.switch_simulation_mode,
            width=120
        )
        mode_option.pack(side="left", padx=5)

    def create_tool_panel(self):
        """ایجاد نوار ابزار سمت چپ جهت افزودن المان‌ها"""
        self.tools_frame = ctk.CTkFrame(self.root, width=200, height=650, fg_color="#d9d9d9")
        self.tools_frame.place(x=10, y=60)

        tool_title = ctk.CTkLabel(self.tools_frame, text="Toolbox", font=("Arial", 16, "bold"))
        tool_title.place(x=20, y=10)

        # دکمه‌های افزودن المان‌های مختلف
        tools = [
            "Button", "Label", "Entry", "Checkbutton",
            "Radiobutton", "Slider", "Textbox", "Progressbar",
            "Combobox", "Switch", "Frame", "Media"
        ]
        start_y = 50
        for tool in tools:
            btn = ctk.CTkButton(
                self.tools_frame,
                text=tool,
                width=160,
                command=lambda t=tool: self.add_element(t)
            )
            btn.place(x=20, y=start_y)
            start_y += 45

    # --------------- بخش شبیه‌ساز (فضای طراحی) ---------------
    def create_simulation_area(self):
        """ایجاد ناحیه شبیه‌ساز در مرکز برنامه با ابعاد ثابت"""
        # در اینجا یک container ثابت برای شبیه‌ساز ایجاد می‌کنیم
        self.simulator_container = ctk.CTkFrame(self.root, width=750, height=650, fg_color="#cccccc")
        self.simulator_container.place(x=220, y=60)
        # جلوگیری از تغییر اندازه container بر اساس فرزندان:
        self.simulator_container.pack_propagate(False)
        self.create_simulator()

    def create_simulator(self):
        """ایجاد فریم شبیه‌ساز ثابت (با ابعاد ثابت) بر اساس مد انتخاب‌شده"""
        # پاکسازی محتویات قبلی (در صورت تغییر مد)
        for widget in self.simulator_container.winfo_children():
            widget.destroy()

        mode = self.simulation_mode.get()
        if mode == "Mobile":
            sim_width, sim_height = 360, 640
            bg_color = "#ffffff"
            border_color = "#000000"
        else:  # Web
            sim_width, sim_height = 700, 600
            bg_color = "#ffffff"
            border_color = "#444444"

        # ایجاد فریم شبیه‌ساز با ابعاد ثابت؛ این فریم تغییر نخواهد کرد
        self.simulator_frame = ctk.CTkFrame(
            self.simulator_container,
            width=sim_width,
            height=sim_height,
            fg_color=bg_color,
            corner_radius=10
        )
        self.simulator_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.simulator_frame.pack_propagate(False)
        try:
            self.simulator_frame.configure(border_color=border_color, border_width=2)
        except Exception:
            pass

        # لیست المان‌های موجود را حفظ می‌کنیم؛ شبیه‌ساز ثابت باقی می‌ماند

    # --------------- پنل تنظیمات و ویرایش ویژگی‌ها ---------------
    def create_properties_panel(self):
        """ایجاد پنل تنظیمات جهت تغییر ویژگی‌های المان انتخاب‌شده"""
        self.properties_frame = ctk.CTkFrame(self.root, width=250, height=650, fg_color="#f1f1f1")
        self.properties_frame.place(x=980, y=60)

        prop_title = ctk.CTkLabel(self.properties_frame, text="Properties", font=("Arial", 16, "bold"))
        prop_title.place(x=20, y=10)

        # متغیرهای تنظیمات
        self.prop_vars = {
            "text": ctk.StringVar(),
            "width": ctk.StringVar(),
            "height": ctk.StringVar(),
            "fg_color": ctk.StringVar(),
            "bg_color": ctk.StringVar(),
            "font": ctk.StringVar()
        }
        labels = {
            "text": "Text:",
            "width": "Width:",
            "height": "Height:",
            "fg_color": "Border Color:",
            "bg_color": "BG Color:",
            "font": "Font:"
        }
        y_pos = 50
        for key, label_text in labels.items():
            lbl = ctk.CTkLabel(self.properties_frame, text=label_text, anchor="w")
            lbl.place(x=10, y=y_pos)
            entry = ctk.CTkEntry(self.properties_frame, textvariable=self.prop_vars[key], width=220)
            entry.place(x=10, y=y_pos + 25)
            y_pos += 60

        # دکمه اعمال تغییرات
        apply_btn = ctk.CTkButton(self.properties_frame, text="Apply Changes", command=self.apply_properties)
        apply_btn.place(x=10, y=y_pos + 10)

        # دکمه ویرایش کد اختصاصی المان
        edit_code_btn = ctk.CTkButton(self.properties_frame, text="Edit Code", command=self.edit_element_code)
        edit_code_btn.place(x=130, y=y_pos + 10)

    # --------------- فریم پایین (تولید کد) ---------------
    def create_bottom_panel(self):
        """ایجاد فریم پایین جهت تولید کد پایتون"""
        self.bottom_frame = ctk.CTkFrame(self.root, width=1200, height=50, fg_color="#d0d0d0")
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        gen_code_btn = ctk.CTkButton(self.bottom_frame, text="Generate Python Code", command=self.generate_code)
        gen_code_btn.pack(padx=20, pady=10, side="left")

    # --------------- مدیریت مد شبیه‌سازی ---------------
    def switch_simulation_mode(self, mode):
        self.simulation_mode.set(mode)
        self.create_simulator()

    # --------------- افزودن المان (با container wrapper) ---------------
    def add_element(self, element_type):
        """
        افزودن المان جدید بر اساس نوع انتخاب‌شده.
        المان در یک container قرار می‌گیرد تا بتوانیم کادر انتخاب (bounding box) داشته باشیم.
        """
        try:
            default_width, default_height = 120, 40
            child = None  # المان واقعی داخل container
            if element_type == "Button":
                child = ctk.CTkButton(self.simulator_frame, text="Button")
            elif element_type == "Label":
                child = ctk.CTkLabel(self.simulator_frame, text="Label")
            elif element_type == "Entry":
                child = ctk.CTkEntry(self.simulator_frame)
                default_width, default_height = 150, 30
            elif element_type == "Checkbutton":
                child = ctk.CTkCheckBox(self.simulator_frame, text="Check")
            elif element_type == "Radiobutton":
                child = ctk.CTkRadioButton(self.simulator_frame, text="Radio")
            elif element_type == "Slider":
                child = ctk.CTkSlider(self.simulator_frame, from_=0, to=100)
                default_width, default_height = 150, 30
            elif element_type == "Textbox":
                child = ctk.CTkTextbox(self.simulator_frame)
                default_width, default_height = 150, 80
            elif element_type == "Progressbar":
                child = ctk.CTkProgressBar(self.simulator_frame)
                default_width, default_height = 150, 30
            elif element_type == "Combobox":
                child = ctk.CTkComboBox(self.simulator_frame, values=["Option 1", "Option 2"])
                default_width, default_height = 150, 30
            elif element_type == "Switch":
                child = ctk.CTkSwitch(self.simulator_frame, text="Switch")
            elif element_type == "Frame":
                child = ctk.CTkFrame(self.simulator_frame, fg_color="#a3c1da", corner_radius=5)
                default_width, default_height = 200, 150
            elif element_type == "Media":
                file_path = filedialog.askopenfilename(
                    title="Select an Image",
                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
                )
                if not file_path:
                    return
                from PIL import Image
                pil_image = Image.open(file_path)
                pil_image = pil_image.resize((150, 100))
                child = ctk.CTkLabel(self.simulator_frame, text="", image=ctk.CTkImage(light_image=pil_image, dark_image=pil_image))
                default_width, default_height = 150, 100
            else:
                return

            # ایجاد container wrapper برای المان
            container = ctk.CTkFrame(
                self.simulator_frame,
                width=default_width,
                height=default_height,
                fg_color="#ffffff",
                border_width=2,
                border_color="#cccccc",  # رنگ اولیه کادر (غیر انتخاب شده)
                corner_radius=4
            )
            container.pack_propagate(False)  # جلوگیری از تغییر اندازه container براساس فرزند

            # قرار دادن المان داخل container
            child.pack(expand=True, fill="both")
            container.child_widget = child  # ذخیره مرجع به المطلب داخل container
            container.widget_type = element_type

            # افزودن قابلیت درگ اند دراپ به container
            self.make_draggable(container)

            # افزودن event انتخاب المان (کلیک راست روی container یا المان داخل آن)
            container.bind("<Button-3>", lambda event, cont=container: self.select_container(cont))
            child.bind("<Button-3>", lambda event, cont=container: self.select_container(cont))

            # قرار دادن container در موقعیت تصادفی داخل شبیه‌ساز (با ابعاد ثابت)
            sim_w = self.simulator_frame.winfo_width() or (360 if self.simulation_mode.get() == "Mobile" else 700)
            sim_h = self.simulator_frame.winfo_height() or (640 if self.simulation_mode.get() == "Mobile" else 600)
            x_pos = random.randint(10, max(10, sim_w - default_width))
            y_pos = random.randint(10, max(10, sim_h - default_height))
            container.place(x=x_pos, y=y_pos)

            # ذخیره المان در لیست
            self.elements.append({
                "container": container,
                "type": element_type,
                "custom_code": ""  # کد اختصاصی برای رویدادها (اختیاری)
            })
        except Exception as e:
            print("Error adding element:", e)

    def make_draggable(self, widget):
        """اعمال قابلیت درگ اند دراپ بر روی container المان‌ها"""
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        """ذخیره مختصات اولیه کلیک برای شروع حرکت"""
        widget = event.widget
        widget._drag_data = {"x": event.x, "y": event.y}
        self.select_container(widget)

    def on_drag_motion(self, event):
        """به‌روزرسانی موقعیت container در هنگام حرکت ماوس بدون تغییر سایز شبیه‌ساز"""
        widget = event.widget
        try:
            dx = event.x - widget._drag_data["x"]
            dy = event.y - widget._drag_data["y"]
        except Exception:
            dx, dy = 0, 0
        new_x = widget.winfo_x() + dx
        new_y = widget.winfo_y() + dy

        # محدودسازی حرکت در داخل شبیه‌ساز (بدون تغییر ابعاد شبیه‌ساز)
        max_x = self.simulator_frame.winfo_width() - widget.winfo_width()
        max_y = self.simulator_frame.winfo_height() - widget.winfo_height()
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))
        widget.place(x=new_x, y=new_y)

    def select_container(self, container):
        """انتخاب یک container (با تغییر رنگ کادر به قرمز) و نمایش ویژگی‌ها در پنل تنظیمات"""
        if self.selected_container and self.selected_container != container:
            self.selected_container.configure(border_color="#cccccc")
        self.selected_container = container
        container.configure(border_color="red")
        self.load_properties(container)

    def load_properties(self, container):
        """بارگذاری ویژگی‌های المان انتخاب‌شده در پنل تنظیمات"""
        try:
            widget = container.child_widget
        except Exception:
            widget = None
        try:
            text_val = widget.cget("text")
        except Exception:
            text_val = ""
        self.prop_vars["text"].set(text_val)
        self.prop_vars["width"].set(str(container.winfo_width()))
        self.prop_vars["height"].set(str(container.winfo_height()))
        try:
            self.prop_vars["fg_color"].set(container.cget("border_color"))
        except Exception:
            self.prop_vars["fg_color"].set("")
        self.prop_vars["bg_color"].set("")  # در صورت نیاز می‌توانید مقداردهی کنید
        try:
            font_val = widget.cget("font")
            if isinstance(font_val, tuple):
                self.prop_vars["font"].set(font_val[0])
            else:
                self.prop_vars["font"].set(font_val)
        except Exception:
            self.prop_vars["font"].set("")

    def apply_properties(self):
        """اعمال تغییرات وارد شده در پنل تنظیمات به المان انتخاب‌شده"""
        if self.selected_container is None:
            messagebox.showwarning("Warning", "No element selected!")
            return

        text = self.prop_vars["text"].get()
        try:
            width_int = int(self.prop_vars["width"].get())
            height_int = int(self.prop_vars["height"].get())
        except ValueError:
            messagebox.showerror("Error", "Width and Height must be integers!")
            return
        fg_color = self.prop_vars["fg_color"].get()
        bg_color = self.prop_vars["bg_color"].get()
        font_name = self.prop_vars["font"].get()

        try:
            self.selected_container.configure(width=width_int, height=height_int)
        except Exception:
            pass
        try:
            self.selected_container.child_widget.configure(text=text)
        except Exception:
            pass
        try:
            if font_name:
                self.selected_container.child_widget.configure(font=(font_name, 12))
        except Exception:
            pass

    def edit_element_code(self):
        """باز کردن پنجره ویرایش کد اختصاصی المان انتخاب‌شده"""
        if self.selected_container is None:
            messagebox.showwarning("Warning", "No element selected!")
            return

        elem = next((item for item in self.elements if item["container"] == self.selected_container), None)
        if elem is None:
            return

        code_window = ctk.CTkToplevel(self.root)
        code_window.title("Edit Element Code")
        code_window.geometry("500x400")

        txt = ctk.CTkTextbox(code_window, wrap="word")
        txt.pack(expand=True, fill="both", padx=10, pady=10)

        previous_code = elem.get("custom_code", "")
        txt.insert("0.0", previous_code)

        def save_code():
            elem["custom_code"] = txt.get("0.0", "end-1c")
            code_window.destroy()

        save_btn = ctk.CTkButton(code_window, text="Save Code", command=save_code)
        save_btn.pack(pady=10)

    # --------------- تولید کد پایتون ---------------
    def generate_code(self):
        """
        تولید کد پایتون کامل جهت بازسازی رابط کاربری ایجاد شده.
        شامل ایجاد containerها، المان‌های داخلی و کد اختصاصی در صورت وجود.
        """
        code_lines = [
            "import customtkinter as ctk",
            "from PIL import Image, ImageTk",
            "",
            "ctk.set_appearance_mode('Light')",
            "ctk.set_default_color_theme('blue')",
            "",
            "root = ctk.CTk()",
            "root.geometry('800x600')",
            "",
            "# Generated UI elements"
        ]

        for idx, item in enumerate(self.elements):
            container = item["container"]
            widget_type = item["type"]
            x = container.winfo_x()
            y = container.winfo_y()
            width = container.winfo_width()
            height = container.winfo_height()
            try:
                child = container.child_widget
                text = child.cget("text")
            except Exception:
                text = ""

            var_name = f"widget_{idx}"
            if widget_type == "Button":
                code_lines.append(f"{var_name} = ctk.CTkButton(root, text='{text}', width={width}, height={height})")
            elif widget_type == "Label":
                code_lines.append(f"{var_name} = ctk.CTkLabel(root, text='{text}', width={width}, height={height})")
            elif widget_type == "Entry":
                code_lines.append(f"{var_name} = ctk.CTkEntry(root, width={width})")
            elif widget_type == "Checkbutton":
                code_lines.append(f"{var_name} = ctk.CTkCheckBox(root, text='{text}')")
            elif widget_type == "Radiobutton":
                code_lines.append(f"{var_name} = ctk.CTkRadioButton(root, text='{text}')")
            elif widget_type == "Slider":
                code_lines.append(f"{var_name} = ctk.CTkSlider(root, from_=0, to=100, width={width})")
            elif widget_type == "Textbox":
                code_lines.append(f"{var_name} = ctk.CTkTextbox(root, width={width}, height={height})")
            elif widget_type == "Progressbar":
                code_lines.append(f"{var_name} = ctk.CTkProgressBar(root, width={width})")
            elif widget_type == "Combobox":
                code_lines.append(f"{var_name} = ctk.CTkComboBox(root, values=['Option 1', 'Option 2'], width={width})")
            elif widget_type == "Switch":
                code_lines.append(f"{var_name} = ctk.CTkSwitch(root, text='{text}')")
            elif widget_type == "Frame":
                code_lines.append(f"{var_name} = ctk.CTkFrame(root, width={width}, height={height}, fg_color='#a3c1da')")
            elif widget_type == "Media":
                code_lines.append(f"# Media element: لطفاً مسیر تصویر را تنظیم کنید")
                code_lines.append(f"{var_name} = ctk.CTkLabel(root, text='', image=ctk.CTkImage(light_image=Image.open('your_image.png'), dark_image=Image.open('your_image.png')))")
            else:
                code_lines.append(f"# Unsupported widget type: {widget_type}")
                continue

            code_lines.append(f"{var_name}.place(x={x}, y={y})")

            custom_code = item.get("custom_code", "").strip()
            if custom_code:
                code_lines.append(f"\n# Custom code for {var_name}")
                code_lines.append(custom_code)
                code_lines.append("")

        code_lines.append("\nroot.mainloop()")

        self.show_code_window("\n".join(code_lines))

    def show_code_window(self, code_text):
        """نمایش کد تولید شده در یک پنجره جداگانه"""
        code_window = ctk.CTkToplevel(self.root)
        code_window.title("Generated Python Code")
        code_window.geometry("600x500")
        text_box = ctk.CTkTextbox(code_window, wrap="word")
        text_box.insert("0.0", code_text)
        text_box.configure(state="disabled")
        text_box.pack(expand=True, fill="both", padx=10, pady=10)


if __name__ == "__main__":
    root = ctk.CTk()
    app = AdvancedAppDesigner(root)
    root.mainloop()
