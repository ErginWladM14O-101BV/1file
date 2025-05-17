import telebot
from telebot import types
import math

TOKEN = '7549231654:AAGB5vZ55NMnUye6eumk5Vm2GLT8ZHpWUpw'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения параметров модели для каждого пользователя
user_params = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_params[chat_id] = {} # Инициализируем словарь параметров для пользователя
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Ввести параметры БПЛА")
    markup.add(item1)
    bot.send_message(chat_id, "Привет! Я бот-калькулятор для БПЛА. Начнем?", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: message.text == "Ввести параметры БПЛА")
def ask_for_parameters(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите размах крыла (м):")
    bot.register_next_step_handler(message, process_wing_span)

def process_wing_span(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['wing_span'] = float(message.text)
        bot.send_message(chat_id, "Введите среднюю хорду крыла (м):")
        bot.register_next_step_handler(message, process_mean_chord)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_wing_span)

def process_mean_chord(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['mean_chord'] = float(message.text)
        bot.send_message(chat_id, "Введите крейсерскую скорость полёта (м/с):")
        bot.register_next_step_handler(message, process_velocity)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_mean_chord)

def process_velocity(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['velocity'] = float(message.text)
        bot.send_message(chat_id, "Введите плотность воздуха (кг/м^3):")
        bot.register_next_step_handler(message, process_air_density)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_velocity)

def process_air_density(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['air_density'] = float(message.text)
        bot.send_message(chat_id, "Введите массу полезной нагрузки (кг):")
        bot.register_next_step_handler(message, process_payload_mass)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_air_density)

def process_payload_mass(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['payload_mass'] = float(message.text)
        bot.send_message(chat_id, "Введите ёмкость аккумулятора (Вт-ч):")
        bot.register_next_step_handler(message, process_battery_capacity_wh)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_payload_mass)

def process_battery_capacity_wh(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['battery_capacity_wh'] = float(message.text)
        bot.send_message(chat_id, "Введите мощность двигателя (Вт):")
        bot.register_next_step_handler(message, process_motor_power_w)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_battery_capacity_wh)

def process_motor_power_w(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['motor_power_w'] = float(message.text)
        bot.send_message(chat_id, "Введите длину фюзеляжа (м):")
        bot.register_next_step_handler(message, process_fuselage_length)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_motor_power_w)

def process_fuselage_length(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['fuselage_length'] = float(message.text)
        bot.send_message(chat_id, "Введите диаметр фюзеляжа (м):")
        bot.register_next_step_handler(message, process_fuselage_diameter)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_fuselage_length)

def process_fuselage_diameter(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['fuselage_diameter'] = float(message.text)
        bot.send_message(chat_id, "Введите длину хвостового оперения (м):")
        bot.register_next_step_handler(message, process_tail_arm)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_fuselage_diameter)

def process_tail_arm(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['tail_arm'] = float(message.text)
        bot.send_message(chat_id, "Введите площадь хвостового оперения (м^2):")
        bot.register_next_step_handler(message, process_tail_area)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_tail_arm)

def process_tail_area(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['tail_area'] = float(message.text)
        bot.send_message(chat_id, "Введите коэффициент лобового сопротивления (базовый):")
        bot.register_next_step_handler(message, process_drag_coefficient)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_tail_area)

def process_drag_coefficient(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['drag_coefficient'] = float(message.text)
        bot.send_message(chat_id, "Введите коэффициент индуктивного сопротивления:")
        bot.register_next_step_handler(message, process_induced_drag_coefficient)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_drag_coefficient)

def process_induced_drag_coefficient(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['induced_drag_coefficient'] = float(message.text)
        bot.send_message(chat_id, "Введите долю массы конструкции от полной массы:")
        bot.register_next_step_handler(message, process_structure_mass_fraction)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_induced_drag_coefficient)

def process_structure_mass_fraction(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['structure_mass_fraction'] = float(message.text)
        bot.send_message(chat_id, "Введите долю массы фюзеляжа от массы конструкции:")
        bot.register_next_step_handler(message, process_fuselage_mass_fraction)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_structure_mass_fraction)

def process_fuselage_mass_fraction(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['fuselage_mass_fraction'] = float(message.text)
        bot.send_message(chat_id, "Введите положение центра масс по длине фюзеляжа:")
        bot.register_next_step_handler(message, process_center_of_mass_position)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_fuselage_mass_fraction)

def process_center_of_mass_position(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['center_of_mass_position'] = float(message.text)
        bot.send_message(chat_id, "Введите угол атаки крыла (градусы):")
        bot.register_next_step_handler(message, process_angle_of_attack_deg)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_center_of_mass_position)

def process_angle_of_attack_deg(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['angle_of_attack_deg'] = float(message.text)
        bot.send_message(chat_id, "Введите максимальную нагрузку в g:")
        bot.register_next_step_handler(message, process_max_g_load)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_angle_of_attack_deg)

def process_max_g_load(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['max_g_load'] = float(message.text)
        bot.send_message(chat_id, "Введите диаметр винта (м):")
        bot.register_next_step_handler(message, process_propeller_diameter)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_max_g_load)

def process_propeller_diameter(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['propeller_diameter'] = float(message.text)
        bot.send_message(chat_id, "Введите шаг винта (м):")
        bot.register_next_step_handler(message, process_propeller_pitch)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_propeller_diameter)

def process_propeller_pitch(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['propeller_pitch'] = float(message.text)
        bot.send_message(chat_id, "Введите количество лопастей винта:")
        bot.register_next_step_handler(message, process_propeller_blades)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_propeller_pitch)

def process_propeller_blades(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['propeller_blades'] = int(message.text)
        bot.send_message(chat_id, "Введите КПД двигателя:")
        bot.register_next_step_handler(message, process_motor_efficiency)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_propeller_blades)

def process_motor_efficiency(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['motor_efficiency'] = float(message.text)
        bot.send_message(chat_id, "Введите КПД винта:")
        bot.register_next_step_handler(message, process_propeller_efficiency)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_motor_efficiency)

def process_propeller_efficiency(message):
    chat_id = message.chat.id
    try:
        user_params[chat_id]['propeller_efficiency'] = float(message.text)
        # Все параметры введены, можно создавать объект модели
        uav = UAVComprehensiveModel(**user_params[chat_id])
        bot.send_message(chat_id, "Параметры приняты. Сейчас произведем расчет...")
        summary = get_uav_summary(uav)
        bot.send_message(chat_id, summary)
    except ValueError:
        bot.send_message(chat_id, "Некорректный формат. Введите число.")
        bot.register_next_step_handler(message, process_propeller_efficiency)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при расчете: {str(e)}")

def get_uav_summary(uav):
    summary = "=== Результаты расчета ===\n"
    summary += f"Размах крыла: {uav.wing_span:.2f} м\n"
    summary += f"Средняя хорда: {uav.mean_chord:.2f} м\n"
    summary += f"Общая масса: {uav.total_mass:.2f} кг\n"
    summary += f"Подъемная сила: {uav.lift_force:.2f} Н\n"
    summary += f"Аэродинамическое качество: {uav.aero_quality:.2f}\n"
    summary += f"Время полета: {uav.flight_time_min:.2f} минут\n"
    summary += f"Потребляемая мощность: {uav.required_power:.2f} Вт\n"
    return summary

# Запуск бота
if __name__ == '__main__':
    from uav_model import UAVComprehensiveModel  # Укажите правильный путь к файлу
    bot.polling(none_stop=True)
