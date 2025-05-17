import math

class UAVComprehensiveModel:
    def __init__(self,
                 wing_span, mean_chord, velocity, air_density,
                 payload_mass, battery_capacity_wh, motor_power_w,
                 fuselage_length, fuselage_diameter,
                 tail_arm, tail_area,
                 cd0=0.02, k=0.05,
                 structural_mass_fraction=0.3,
                 fuselage_mass_fraction=0.2,
                 cg_position_fraction=0.25,
                 angle_of_attack_deg=4,
                 max_load_factor=6,
                 propeller_diameter=0.3,
                 propeller_pitch=0.2,
                 number_of_blades=2,
                 efficiency_motor=0.9,
                 efficiency_prop=0.85,
                 gravity=9.81):
        # Инициализация параметров (как в вашем исходном коде)...
        self.wing_span = wing_span
        self.mean_chord = mean_chord
        self.wing_area = self.wing_span * self.mean_chord
        self.aspect_ratio = self.wing_span ** 2 / self.wing_area

        self.fuselage_length = fuselage_length
        self.fuselage_diameter = fuselage_diameter
        self.tail_arm = tail_arm
        self.tail_area = tail_area

        # Полётные параметры
        self.velocity = velocity
        self.air_density = air_density
        self.angle_of_attack_deg = angle_of_attack_deg
        self.angle_of_attack_rad = math.radians(angle_of_attack_deg)

        # Массы и мощности
        self.payload_mass = payload_mass
        self.battery_capacity_wh = battery_capacity_wh
        self.motor_power_w = motor_power_w
        self.structural_mass_fraction = structural_mass_fraction
        self.fuselage_mass_fraction = fuselage_mass_fraction

        # Коэффициенты аэродинамики
        self.cd0 = cd0
        self.k = k

        # Максимальная нагрузка (g)
        self.max_load_factor = max_load_factor

        # Винт и силовая установка
        self.propeller_diameter = propeller_diameter
        self.propeller_pitch = propeller_pitch
        self.number_of_blades = number_of_blades
        self.efficiency_motor = efficiency_motor
        self.efficiency_prop = efficiency_prop

        self.gravity = gravity

        # Расчёты масс
        self.calculate_masses()

        # Аэродинамические коэффициенты с учётом угла атаки
        self.lift_coefficient, self.drag_coefficient, self.lift_drag_ratio = self.calc_aero_coefficients_from_aoa()

        # Расчёты аэродинамики и сил
        self.calculate_lift()
        self.calculate_drag()
        self.calculate_aero_quality()
        self.calculate_wing_loading()

        # Центр масс и устойчивость
        self.calculate_center_of_gravity()
        self.calculate_stability_margin()

        # Момент инерции и динамика
        self.calculate_moment_of_inertia()
        self.calculate_pitching_moment()

        # Энергетика и время полёта
        self.calculate_flight_time()
        self.calculate_power_requirements()

        # Конструкция и прочность
        self.calculate_structural_safety_factor()

        # Управление и устойчивость
        self.calculate_control_derivatives_approx()

        # Оптимальное расположение двигателя
        self.optimal_engine_position = self.calculate_optimal_engine_position()

        # Траектория и навигация (базовые функции)
        self.flight_path = []

    def calculate_masses(self):
        battery_specific_energy = 200  # Вт·ч/кг для LiPo
        self.battery_mass = self.battery_capacity_wh / battery_specific_energy
        self.structural_mass = self.structural_mass_fraction * (self.payload_mass + self.battery_mass) / (1 - self.structural_mass_fraction)
        self.fuselage_mass = self.fuselage_mass_fraction * self.structural_mass
        motor_mass = 0.1 * self.motor_power_w / 1000  # кг (приблизительно)
        self.total_mass = self.structural_mass + self.payload_mass + self.battery_mass + self.fuselage_mass + motor_mass

    def calc_aero_coefficients_from_aoa(self):
        data = {
            -4: (-0.0323, 0.0633, 0.5097),
             0: (0.8888, 0.0679, 13.0988),
             4: (1.7661, 0.1209, 14.6025),
             8: (2.3706, 0.2142, 11.0674),
            12: (2.1060, 0.3749, 5.6176),
            16: (1.9047, 0.5187, 3.6719),
            20: (1.8456, 0.6968, 2.6487),
        }
        aoa = self.angle_of_attack_deg
        keys = sorted(data.keys())
        for i in range(len(keys)-1):
            if keys[i] <= aoa <= keys[i+1]:
                x0, x1 = keys[i], keys[i+1]
                cl0, cd0, ld0 = data[x0]
                cl1, cd1, ld1 = data[x1]
                factor = (aoa - x0) / (x1 - x0)
                cl = cl0 + factor * (cl1 - cl0)
                cd = cd0 + factor * (cd1 - cd0)
                ld = ld0 + factor * (ld1 - ld0)
                return cl, cd, ld
        if aoa < keys[0]:
            return data[keys[0]]
        else:
            return data[keys[-1]]

    def calculate_lift(self):
        weight = self.total_mass * self.gravity
        self.lift = weight
        self.lift_force = 0.5 * self.air_density * self.velocity ** 2 * self.wing_area * self.lift_coefficient

    def calculate_drag(self):
        self.drag_force = 0.5 * self.air_density * self.velocity ** 2 * self.wing_area * self.drag_coefficient

    def calculate_aero_quality(self):
        self.aero_quality = self.lift_coefficient / self.drag_coefficient

    def calculate_wing_loading(self):
        self.wing_loading = self.total_mass / self.wing_area

    def calculate_center_of_gravity(self):
        cg_fuselage = 0.5 * self.fuselage_length
        cg_payload = 0.75 * self.fuselage_length
        cg_battery = 0.4 * self.fuselage_length
        total = self.structural_mass + self.fuselage_mass + self.payload_mass + self.battery_mass
        self.cg_position = (self.structural_mass * cg_fuselage +
                            self.fuselage_mass * cg_fuselage +
                            self.payload_mass * cg_payload +
                            self.battery_mass * cg_battery) / total

    def calculate_stability_margin(self):
        aerodynamic_center = 0.25 * self.mean_chord
        self.stability_margin = self.cg_position - aerodynamic_center

    def calculate_moment_of_inertia(self):
        self.moment_of_inertia = (1/12) * self.total_mass * self.wing_span ** 2

    def calculate_pitching_moment(self):
        cm_alpha = -1.2
        self.pitching_moment = cm_alpha * self.angle_of_attack_rad * 0.5 * self.air_density * self.velocity ** 2 * self.wing_area * self.mean_chord

    def calculate_flight_time(self):
        efficiency_total = self.efficiency_motor * self.efficiency_prop
        self.flight_time_min = (self.battery_capacity_wh / self.motor_power_w) * efficiency_total * 60

    def calculate_power_requirements(self):
        self.required_power = self.drag_force * self.velocity / (self.efficiency_prop * self.efficiency_motor)

    def calculate_structural_safety_factor(self):
        max_load = self.max_load_factor * self.total_mass * self.gravity
        design_load = 1.5 * max_load
        self.safety_factor = design_load / max_load

    def calculate_control_derivatives_approx(self):
        self.cL_alpha = 5.5
        self.cD_alpha = 0.3
        self.cm_alpha = -1.2
        self.cY_beta = -0.5
        self.cl_beta = -0.1
        self.cn_beta = 0.2

    def calculate_optimal_engine_position(self):
        x = 0.25 * self.mean_chord
        y = 0.5 * self.wing_span
        return x, y

    def calculate_optimal_components_layout(self):
        layout = {}
        engine_x = 0.25 * self.mean_chord
        engine_y1 = 0.25 * self.wing_span
        engine_y2 = 0.75 * self.wing_span
        layout['engine_1'] = {'x': engine_x, 'y': engine_y1}
        layout['engine_2'] = {'x': engine_x, 'y': engine_y2}
        layout['battery'] = {'x': 0.4 * self.fuselage_length}
        layout['payload'] = {'x': 0.7 * self.fuselage_length}
        layout['electronics'] = {'x': 0.5 * self.fuselage_length}
        layout['wing'] = {'x': 0.5 * self.fuselage_length}
        layout['tail'] = {'x': self.fuselage_length}
        return layout

    def print_optimal_layout(self):
        layout = self.calculate_optimal_components_layout()
        print("\n--- Оптимальное расположение элементов (по длине фюзеляжа) ---")
        print(f"{'Элемент':<15} {'X (м)':>10} {'Y (м)':>10}")
        for key, pos in layout.items():
            x = pos.get('x', '-')
            y = pos.get('y', '-')
            if y == '-':
                print(f"{key:<15} {x:>10.2f} {y:>10}")
            else:
                print(f"{key:<15} {x:>10.2f} {y:>10.2f}")

    def calculate_distance(self, start, end):
        return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

    def calculate_flight_direction(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[0]
        angle_rad = math.atan2(dy, dx)
        return math.degrees(angle_rad)

    def calculate_flight_time_to_point(self, start, end):
        distance = self.calculate_distance(start, end)
        return distance / self.velocity

    def simulate_flight(self, start, end, time_step=1.0):
        direction_deg = self.calculate_flight_direction(start, end)
        direction_rad = math.radians(direction_deg)
        distance = self.calculate_distance(start, end)
        total_time = distance / self.velocity
        steps = int(total_time / time_step)
        path = []
        for step in range(steps + 1):
            t = step * time_step
            x = start[0] + self.velocity * t * math.cos(direction_rad)
            y = start[1] + self.velocity * t * math.sin(direction_rad)
            path.append((x, y))
        self.flight_path = path
        return path

    def print_summary(self):
        print("=== Полный расчёт параметров беспилотника ===")
        print(f"Размах крыла:               {self.wing_span:.2f} м")
        print(f"Средняя хорда:              {self.mean_chord:.2f} м")
        print(f"Общая масса:                {self.total_mass:.2f} кг")
        print(f"Подъёмная сила:            {self.lift_force:.2f} Н")
        print(f"Коэффициент подъёмной силы: {self.lift_coefficient:.2f}")
        print(f"Коэффициент лобового сопротивления: {self.drag_coefficient:.2f}")
        print(f"Аэродинамическое качество: {self.aero_quality:.2f}")
        print(f"Удельная нагрузка на крыло: {self.wing_loading:.2f} кг/м^2")
        print(f"Запас устойчивости:        {self.stability_margin:.2f} м")
        print(f"Момент инерции:            {self.moment_of_inertia:.2f} кг*м^2")
        print(f"Крутящий момент:           {self.pitching_moment:.2f} Н*м")
        print(f"Расчётное время полёта:    {self.flight_time_min:.2f} мин")
        print(f"Потребляемая мощность:     {self.required_power:.2f} Вт")
        print(f"Коэффициент безопасности:  {self.safety_factor:.2f}")
        self.print_optimal_layout()

# Функция для обработки команды /calculate
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Пример параметров для инициализации модели
        wing_span = 2.0  # м
        mean_chord = 0.2  # м
        velocity = 20.0  # м/с
        air_density = 1.225  # кг/м^3
        payload_mass = 1.0  # кг
        battery_capacity_wh = 200  # Вт·ч
        motor_power_w = 300  # Вт
        fuselage_length = 1.5  # м
        fuselage_diameter = 0.15  # м
        tail_arm = 0.5  # м
        tail_area = 0.1  # м

        # Создаем экземпляр класса UAVComprehensiveModel
        uav_model = UAVComprehensiveModel(wing_span, mean_chord, velocity, air_density,
                                          payload_mass, battery_capacity_wh, motor_power_w,
                                          fuselage_length, fuselage_diameter,
                                          tail_arm, tail_area)

        # Получаем результаты расчетов в виде строки
        # Вместо вывода в консоль, собираем результаты в строку
        summary_text = "=== Полный расчёт параметров беспилотника ===\n"
        summary_text += f"Размах крыла:               {uav_model.wing_span:.2f} м\n"
        summary_text += f"Средняя хорда:              {uav_model.mean_chord:.2f} м\n"
        summary_text += f"Общая масса:                {uav_model.total_mass:.2f} кг\n"
        summary_text += f"Подъёмная сила:            {uav_model.lift_force:.2f} Н\n"
        summary_text += f"Коэффициент подъёмной силы: {uav_model.lift_coefficient:.2f}\n"
        summary_text += f"Коэффициент лобового сопротивления: {uav_model.drag_coefficient:.2f}\n"
        summary_text += f"Аэродинамическое качество: {uav_model.aero_quality:.2f}\n"
        summary_text += f"Удельная нагрузка на крыло: {uav_model.wing_loading:.2f} кг/м^2\n"
        summary_text += f"Запас устойчивости:        {uav_model.stability_margin:.2f} м\n"
        summary_text += f"Момент инерции:            {uav_model.moment_of_inertia:.2f} кг*м^2\n"
        summary_text += f"Крутящий момент:           {uav_model.pitching_moment:.2f} Н*м\n"
        summary_text += f"Расчётное время полёта:    {uav_model.flight_time_min:.2f} мин\n"
        summary_text += f"Потребляемая мощность:     {uav_model.required_power:.2f} Вт\n"
        summary_text += f"Коэффициент безопасности:  {uav_model.safety_factor:.2f}\n\n"

        layout = uav_model.calculate_optimal_components_layout()
        summary_text += "--- Оптимальное расположение элементов (по длине фюзеляжа) ---\n"
        summary_text += f"{'Элемент':<15} {'X (м)':>10} {'Y (м)':>10}\n"
        for key, pos in layout.items():
            x = pos.get('x', '-')
            y = pos.get('y', '-')
            if y == '-':
                summary_text += f"{key:<15} {x:>10.2f} {y:>10}\n"
            else:
                summary_text += f"{key:<15} {x:>10.2f} {y:>10.2f}\n"

        # Отправляем результаты пользователю
        await update.message.reply_text(summary_text)

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для расчета параметров БПЛА. Используйте команду /calculate для расчета.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчики команд
    start_handler = CommandHandler('start', start)
    calculate_handler = CommandHandler('calculate', calculate)

    application.add_handler(start_handler)
    application.add_handler(calculate_handler)

    application.run_polling()
