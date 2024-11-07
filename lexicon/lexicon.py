LEXICON: dict[str, str] = {'/start': '<b>📉Приветствую, я бот-скринер, '
                                     'который сообщает об изменении цены</b>📈\n\n'
                                     '🛠Доступны три настройки🛠:\n\n'
                                     '🟢<b>ПАМП</b>🟢 (пик) сильное изменение цены '
                                     'за определённый промежуток - позволяет найти '
                                     'монеты на пике пампа, чтобы открыть ШОРТ позицию (и заработать на откате вниз).\n\n'
                                     '💹<b>ЛОНГ</b>💹 (начало) быстрое изменение цены за короткий промежуток - '
                                     'позволяет поймать начало Пампа, чтобы открыть ЛОНГ позицию (и заработать на продолжении движения).\n\n'
                                     '🔴<b>ДАМП</b>🔴 сильное падение цены за определённый промежуток - позволяет найти '
                                     'монеты после пампа, чтобы открыть ЛОНГ позицию (и заработать на откате вверх).\nСвязь с нами @pump_support_byHavi\n\n'
                                     '<b>💳Для активации подписки пройдите в соответсвующий раздел или воспользуйтесь командой /pay 🔐</b>',
                           '/help': 'Помощь🆘',
                           '/setting': 'Настройки🔧',
                           '/profile': 'Профиль📇',
                           '/pump': '🟢ПАМП🔧',
                           '/dump': '🔴ДАМП🔧',
                           '/long': '💹ЛОНГ🔧',
                           '/pay': '🔐Подписка',
                           '/quantity': '🧿Кол-во сигналов🔧',
                           '/chanel': '❌Отмена❌',
                           '/hours_24': 'За 24 часа🕛',
                           '/hours_12': 'За 12 часов🕛',
                           '/hours_6': 'За 6 часов🕕',
                           '/on_limited': 'Без ограничений🔄',
                           '/bybit': 'ByBit🟢',
                           '/binance': 'Binance🟢',
                           '/bybit_off': 'ByBit🔴',
                           '/binance_off': 'Binance🔴',
                           '/market': 'Биржа📊',
                           '/prem': '🔐Подписка',
                           'pay_crypto':'💎Оплатить криптовалютой',
                           'pay': '🔓Доступ на 30 дней 10$',
                           'pay_90': 'Доступ на 90 дней ',
                           'free_play': '🎟Пробный период на 1 день',
                           'chanel': '🆓Бесплатный канал с сигналами',
                           '/quantity_pd': '🧿Сигналы ПАМП🟢 ДАМП🔴',
                           '/quantity_pm': '🧿Сигналы ЛОНГ💹'
                           }

LEXICON_TEXT: dict[str, str] = {'setting_text': '🔧Текущие настройки:🔧\n\n'
                                                '🟢<b>ПАМП</b>: {changes_long} % за {interval_long} минут🟢\n\n'
                                                '🔴<b>ДАМП</b>: {changes_short} % за {interval_short} минут🔴\n\n'
                                                '{quantity_text}\n\n----------\n\n'
                                                '💹<b>ЛОНГ</b>: {changes_long_min} % за {intarval_long_min} минут💹\n\n'
                                                '{quantity_text_min}',
                                'setting_text_on_limit': '🔧Текущие настройки:🔧\n\n'
                                                      '🟢<b>ПАМП</b>: {changes_long} % за {interval_long} минут🟢\n\n'
                                                      '🔴<b>ДАМП</b>: {changes_short} % за {interval_short} минут🔴\n\n'
                                                      '💹<b>ЛОНГ</b>: {changes_long_min} % за {intarval_long_min} минут💹\n\n'
                                                      '🧿Количество <b>ПАМП</b> и <b>ДАМП</b> сигналов без ограничений🧿',
                                'long_setting_changes': '<b>📈Установите рост цены от 1 до 9999 процентов</b>📈',
                                'setting_interval': '<b>✅Изменение цены установлено✅</b>\n\n'
                                                    '⏳<b>Установите период от 1 до 120 минут</b>',
                                'short_setting_changes': '📉<b>Установите падение цены от 1 до 9999 процентов</b>📉',
                                'warning_long_changes': '📛<b>Рост цены должено быть целым числом от 1 до 9999</b>📛\n\n'
                                                        'Попробуйте еще раз\n\n'
                                                        'Если вы хотите прервать настройку'
                                                        ' - нажмите кнопку "❌<b>Отмена</b>❌"',
                                'warning_short_changes': '📛<b>Падение цены должено быть целым числом от 1 до 9999</b>📛\n\n'
                                                         'Попробуйте еще раз\n\n'
                                                         'Если вы хотите прервать настройку - нажмите кнопку "❌<b>Отмена</b> ❌"',
                                'warning_interval': '📛<b>Интервал времени должен быть целым числом от 1 до 120</b>📛\n\n'
                                                    'Попробуйте еще раз\n\n'
                                                    'Если вы хотите прервать настройку интервала времени - нажмите кнопку "❌<b>Отмена</b> ❌"',
                                'new_setting_q': '<b>✅Настройки количество сигналовсигналов изменены, текущие настройки:</b>\n\n'
                                                 '🟢<b>ПАМП: {changes_long} % за {interval_long} минут </b>🟢\n\n'
                                                 '🔴<b>ДАМП: {changes_short} % за {interval_short} минут </b>🔴\n\n'
                                                 '🧿<b>Количество сигналов за {quantity_interval} {hours_text}: {quantity_setting}</b>🧿',
                                'chanel': '❌<b>Настройки отменены</b>❌',
                                'quantity_interval': '⏳<b>Выбирите период сигналов</b>⏳',
                                'quantity_setting': '🧿<b>Введите количество сигналов за выбранный вами период</b>🧿',
                                'quantity_warning_setting': '📛<b>Количество сигналов должно быть целым положительным числом</b>📛\n'
                                                            'Введите целое число или нажмите кнопку "❌<b>Отмена настроек</b>❌"',
                                'quantity_warning': 'Выберите период или нажмите кнопку "❌<b>Отмена</b>❌"',
                                'new_setting': '<b>✅Настройки сигналов изменены, текущие настройки:</b>\n\n'
                                               '🟢<b>ПАМП: {changes_long} % за {interval_long} минут </b>🟢\n\n'
                                               '🔴<b>ДАМП: {changes_short} % за {interval_short} минут </b>🔴\n\n'
                                               '💹ЛОНГ: {changes_long_min} % за {intarval_long_min} минут💹\n\n'
                                               '🧿Количество сигналов за {quantity_interval} {hours_text}: {quantity_setting}🧿',
                                'quantity_on_limited': '<b>✅Настройки количество сигналовсигналов изменены, текущие настройки:</b>\n\n'
                                                       '🟢<b>ПАМП: {changes_long} % за {interval_long} минут </b>🟢\n\n'
                                                       '🔴<b>ДАМП: {changes_short} % за {interval_short} минут </b>🔴\n\n'
                                                       '💹ЛОНГ: {changes_long_min} % за {intarval_long_min} минут💹\n\n'
                                                       '🧿<b>Количество сигналов без ограничений</b>🧿',
                                'new_setting_no_limited': '<b>✅Настройки сигналов изменены, текущие настройки</b>✅:\n\n'
                                                         '🟢<b>ПАМП: {changes_long} % за {interval_long} минут </b>🟢'
                                                         '\n\n🔴<b>ДАМП: {changes_short} % за {interval_short} минут</b>🔴'
                                                          '💹ЛОНГ: {changes_long_min} % за {intarval_long_min} минут💹\n\n'
                                                         '\n\n🧿<b>Количество сигналов без ограничений</b>🧿',
                                'premium': '<b>Ваша подписка действительна до {prm_date}(UTC=0)\nТакже в подписку входит второй бот @open_interes_bybot</b>\nСвязь с нами @pump_support_byHavi',
                                'premium_pay': '<b>✅ПОДПИСКА АКТИВНА до {prm_date}(UTC=0)✅</b>',
                                'fail_premium': '<b>Подписка отсутсвует, вы можете оплатить ее криптавалютой в соотвествующем меню или пишите в ЛС @pump_support_byHavi</b>',
                                'market': '<b>Выбирите биржу, которую хотите отключить🔴 или включить🟢 (🟢 - биржа активна)</b>',
                                'help': '<b>Это бот для сигналов роста и падения цены.\n'
                                        'После первого старта вам доступна бесплатная подписка 1 день, которую можно активировать командой /pay или в разделе <b>🔐Подписка.</b>\n'
                                        'Доступны следующие команды:\n'
                                        '/reset - команда сбросит настройки сигналов до стартовых\n'
                                        '/setting - вызов панели настройки🔧 сигналов\n'
                                        '/chanel - ❌отмена любого действия\n\n'
                                        'Все настройки позиций устаналиваются отправкой целых положительных чисел в чат,'
                                        'после того как на панели будет выбрана соответствуюущая настройка\n'
                                        'Бот отркытого интереса @open_interes_bybot\n</b>\n'
                                        'Связь с нами @pump_support_byHavi',
                                'pay_30': '<b>После оплаты вам будет открыт доступ на 30 дней</b>',
                                'free_play': '<b>Вы уже использовали пробдный период</b>',
                                'free_play_on': '<b>✅Пробдный период активирован✅</b>',
                                'not_prem': '<b>Подписка отсутсвует, вы можете оплатить ее криптавалютой в соотвествующем меню, для оплаты другими способами пишите в ЛС @pump_support_byHavi</b>',
                                'qunatity_pd_pm': 'Выберите для каких сигналов нужно настроить количество для 🟢<b>ПАМП, 🔴ДАМП</b> или для <b>💹ЛОНГ</b>'
                                }

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Запуск бота',
    '/setting': 'Настройки сигналов',
    '/reset': 'Настройки по умолчанию',
    '/help': 'Описание бота'}