/**
 *  author:   Yuriy Lobarev
 *  telegram: @forman
 *  phone:    +7(910)983-95-90
 *  email:    forman@anyks.com
 *  site:     https://anyks.com
 */

#ifndef _ANYKS_SC_
#define _ANYKS_SC_

/**
 * Системные модули
 */
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
/**
 * Наши модули
 */
#include <alm.hpp>
#include <spl.hpp>
#include <ascb.hpp>
#include <toolkit.hpp>
#include <collector.hpp>

// Устанавливаем область видимости
using namespace std;
// Устанавливаем область видимости
namespace py = pybind11;
// Активируем пространство имён json
using json = nlohmann::json;
// Устанавливаем конвертер типов данных
template <typename... Args>
using overload_cast_ = py::detail::overload_cast_impl <Args...>;
/**
 * anyks пространство имён
 */
namespace anyks {
	// Флаги удаления в слове
	enum class wdel_t : u_short {
		punct,  // Флаг удаления знаков пунктуации в слове
		broken, // Флаг удаления плохих слов в слове
		hyphen  // Флаг удаления дефисов в слове
	};
	// Флаги очистики
	enum class clear_t : u_short {
		all,      // Флаг полной очистки
		utokens,  // Флаг очистки пользовательских токенов
		badwords, // Флаг очистки чёрного списка
		goodwords // Флаг очистки белого списка
	};
	// Флаги проверки
	enum class check_t : u_short {
		home2,   // Флаг проверки слова по типу Дом-2
		latian,  // Флаг проверки на наличие латинского символа
		hyphen,  // Флаг проверки на наличие доефиса
		letter,  // Флаг проверки легальности буквы
		similars // Флаг проверки смешанных букв разных словарей
	};
	// Флаги типов сглаживания
	enum class smoothing_t : u_short {
		wittenBell,     // WittenBell
		addSmooth,      // AddSmooth
		kneserNey,      // KneserNey
		goodTuring,     // GoodTuring
		modKneserNey,   // ModKneserNey
		constDiscount,  // ConstDiscount
		naturalDiscount // NaturalDiscount
	};
	// Основные опции
	enum class options_t : u_int {
		debug,       // Флаг режима отладки
		bloom,       // Флаг разрешающий использовать фильтр Блума
		stress,      // Флаг разрешения использовать символы ударения
		uppers,      // Флаг разрешения проставлять регистры букв в словах
		collect,     // Флаг разрешения сборку суффиксов цифровых аббревиатур
		stemming,    // Флаг активации стемминга
		onlyGood,    // Флаг использования только слов из белого списка
		mixdicts,    // Флаг разрешающий детектировать слова из смешанных словарей
		allowUnk,    // Флаг разрешения использовать токен неизвестного слова
		resetUnk,    // Флаг разрешения сбрасывать частоту токена неизвестного слова
		allGrams,    // Флаг разрешения использовать абсолютно все полученные n-граммы
		onlytypos,   // Флаг исправления только опечаток
		lowerCase,   // Флаг разрешения переводить слова в нижний регистр
		confidence,  // Флаг разрешающий загружать n-граммы из arpa так-как они есть
		tokenWords,  // Флаг учитывающий при сборке N-грамм, только те токены, которые соответствуют словам
		interpolate, // Флаг разрешения выполнять интерполяцию при расчёте arpa
		ascsplit,    // Флаг режима разрешения выполнять сплитов текста
		ascalter,    // Флаг разрешения на исправление слов с альтернативными буквами
		ascesplit,   // Флаг разрешения использовать сплиты с ошибками
		ascrsplit,   // Флаг разрешения на удаление сплитов в словах
		ascuppers,   // Флаг разрешения проставлять регистры в словах
		aschyphen,   // Флаг разрешения выполнять сплиты по дефисам
		ascskipupp,  // Флаг пропуска слов в верхнем регистре
		ascskiplat,  // Флаг пропуска слов с латинскими символами
		ascskiphyp,  // Флаг пропуска слова с дефисами
		ascwordrep   // Флаг удаления повторяющиеся одинаковых слов
	};
	// Флаги соответствия
	enum class match_t : u_int {
		url,      // Флаг проверки соответствия слова url адресу
		abbr,     // Флаг проверки на соответствие слова аббревиатуре
		math,     // Флаг определения математических операий
		upper,    // Флаг проверки символ на верхний регистр
		punct,    // Флаг проверки является ли буква, знаком препинания
		greek,    // Флаг првоерки является ли буква, символом греческого алфавита
		space,    // Флаг проверки является ли буква, пробелом
		route,    // Флаг проверки является ли буква, символом направления (стрелки)
		latian,   // Флаг проверки является ли строка латиницей
		number,   // Флаг проверки является ли слово числом
		letter,   // Флаг првоерки является ли буква валидной (существует в словаре)
		pcards,   // Флаг првоерки является ли буква игральной картой
		anumber,  // Флаг проверки является ли косвенно слово числом
		allowed,  // Флаг проверки соответствия слова словарю
		decimal,  // Флаг проверки является ли слово дробным числом
		special,  // Флаг определения спец-символа
		currency, // Флаг проверки является ли буква, символом мировой валюты
		isolation // Флаг определения знака изоляции (кавычки, скобки)
	};
	// Тип используемой языковой модели
	bool almV2 = false;
	// Адрес лог файла
	string logfile = "";
	// Объект левенштейна
	lev_t algorithms;
	// Создаём объект алфавита
	alphabet_t alphabet;
	// Флаг инициализация тулкита
	bool toolkitInit = false;
	// Размер длины N-граммы
	u_short order = DEFNGRAM;
	// Общие настройки всех систем
	bitset <26> generalOptions;
	// Основные опции спеллчекера и количество потоков для работы
	size_t options = 0, threads = 0;
	// Создаём объект токенизатора
	tokenizer_t tokenizer(&alphabet);
	// Список альтернативных букв
	map <wchar_t, wchar_t> altLetters;
	// Локаль по умолчанию
	string deflocale = ALPHABET_LOCALE;
	// Список альтернативных слов
	unordered_map <string, string> altWords;
	// Создаём объект тулкита языковой модели
	toolkit_t toolkit(&alphabet, &tokenizer, DEFNGRAM);
	// Создаём обхъект языковой модели ALMv1
	unique_ptr <alm_t> alm1(new alm1_t(&alphabet, &tokenizer));
	// Создаём обхъект языковой модели ALMv2
	unique_ptr <alm_t> alm2(new alm2_t(&alphabet, &tokenizer));
	// Создаём словарь для работы спеллчекера ALMv1
	dict_t dict1(alm1.get(), &alphabet, &tokenizer);
	// Создаём словарь для работы спеллчекера ALMv2
	dict_t dict2(alm2.get(), &alphabet, &tokenizer);
	// Создаём объект спеллчекера ALMv1
	spell_t spell1(&dict1, alm1.get(), &alphabet, &tokenizer);
	// Создаём объект спеллчекера ALMv2
	spell_t spell2(&dict2, alm2.get(), &alphabet, &tokenizer);
	/**
	 * Methods Основные методы библиотеки
	 */
	namespace Methods {
		/**
		 * clear Метод очистки
		 */
		void clear(clear_t flag = clear_t::all){
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем полную очистку
				case u_short(clear_t::all): {
					// Очищаем данные туллкита
					toolkit.clear();
					// Очищаем словарь
					alphabet.clear();
					// Очищаем данные токенизатора
					tokenizer.clear();
					// Сбрасываем флаг инициализации тулкита
					toolkitInit = false;
					// Очищаем языковую модель
					(almV2 ? alm2->clear() : alm1->clear());
					// Очищаем данные словаря
					(almV2 ? dict2.clear() : dict1.clear());
				} break;
				// Выполняем очистку чёрного списка слов
				case u_short(clear_t::badwords): (almV2 ? alm2->clearBadwords() : alm1->clearBadwords()); break;
				// Выполняем очистку пользовательских токенов
				case u_short(clear_t::utokens): (almV2 ? alm2->clearUserTokens() : alm1->clearUserTokens()); break;
				// Выполняем очистку белого списка слов
				case u_short(clear_t::goodwords): (almV2 ? alm2->clearGoodwords() : alm1->clearGoodwords()); break;
			}
		}
		/**
		 * setAlmV2 Метод установки типа языковой модели
		 */
		void setAlmV2() noexcept {
			// Очищаем все данные
			clear();
			// Устанавливаем тип языковой модели 2
			almV2 = true;
		}
		/**
		 * unsetAlmV2 Метод установки типа языковой модели
		 */
		void unsetAlmV2() noexcept {
			// Очищаем все данные
			clear();
			// Отключаем тип языковой модели 2
			almV2 = false;
		}
		/**
		 * switchAllowApostrophe Метод разрешения или запрещения апострофа как части слова
		 */
		void switchAllowApostrophe() noexcept {
			// Выполняем переключение разрешения апострофа
			alphabet.switchAllowApostrophe();
		}
		/**
		 * allowStress Метод разрешения, использовать ударение в словах
		 */
		void allowStress() noexcept {
			// Разрешаем использовать ударение в словах
			tokenizer.setOption(tokenizer_t::options_t::stress);
		}
		/**
		 * disallowStress Метод запрещения использовать ударение в словах
		 */
		void disallowStress() noexcept {
			// Запрещаем использовать ударение в словах
			tokenizer.unsetOption(tokenizer_t::options_t::stress);
		}
		/**
		 * setSize Метод установки размера n-граммы
		 * @param size размер n-граммы
		 */
		void setSize(const u_short size = DEFNGRAM) noexcept {
			// Запоминаем размер длины N-граммы
			order = size;
			// Устанавливаем новый размер длины N-граммы
			toolkit.setSize(size);
			// Устанавливаем новый размер длины N-граммы
			(almV2 ? alm2->setSize(size) : alm1->setSize(size));
		}
		/**
		 * setLocale Метод установки локали
		 * @param locale локализация приложения
		 */
		void setLocale(const string & locale = "en_US.UTF-8") noexcept {
			// Устанавливаем локаль
			if(!locale.empty()) deflocale = locale;
			// Устанавливаем переданную локаль
			alphabet.setlocale(deflocale);
		}
		/**
		 * setAlphabet Метод установки алфавита
		 * @param text алфавит символов для текущего языка
		 */
		void setAlphabet(const wstring & text) noexcept {
			// Устанавливаем алфавит
			alphabet.set(alphabet.convert(text));
			// Обновляем токенайзер
			tokenizer.update();
		}
		/**
		 * setLogfile Метод установки файла для вывода логов
		 * @param file адрес файла для вывода отладочной информации
		 */
		void setLogfile(const wstring & file) noexcept {
			// Если адрес логов передан
			if(!file.empty()){
				// Запоминаем адрес файла логов
				logfile = alphabet.convert(file);
				// Выполняем установку файла для вывода логов
				toolkit.setLogfile(logfile.c_str());
				// Выполняем установку файла для вывода логов токенизатору
				tokenizer.setLogfile(logfile.c_str());
				// Выполняем установку файла для вывода логов
				(almV2 ? alm2->setLogfile(logfile.c_str()) : alm1->setLogfile(logfile.c_str()));
				// Выполняем установку файла для вывода логов словаря
				(almV2 ? dict2.setLogfile(logfile.c_str()) : dict1.setLogfile(logfile.c_str()));
				// Выполняем установку файла для вывода логов спеллчекера
				(almV2 ? spell2.setLogfile(logfile.c_str()) : spell1.setLogfile(logfile.c_str()));
			}
		}
		/**
		 * setOption Метод установки опций модуля
		 * @param option опция для установки
		 */
		void setOption(const options_t option) noexcept {
			// Устанавливаем общие настройки
			generalOptions.set((u_int) option);
			// Устанавливаем нужный нам тип настроек
			switch((u_int) option){
				// Если включён режим отладки
				case (u_int) options_t::debug: {
					// Устанавливаем режим отладки
					toolkit.setOption(toolkit_t::options_t::debug);
					// Устанавливаем режим отладки для токенизатора
					tokenizer.setOption(tokenizer_t::options_t::debug);
					// Включаем режим отладки для спеллчекера
					options = spell1.setOption(spell_t::options_t::debug, options);
					// Устанавливаем режим отладки языковой модели
					(almV2 ? alm2->setOption(alm_t::options_t::debug) : alm1->setOption(alm_t::options_t::debug));
					// Устанавливаем режим отладки словаря
					(almV2 ? dict2.setOption(dict_t::options_t::debug) : dict1.setOption(dict_t::options_t::debug));
				} break;
				// Устанавливаем флаг разрешения использовать символы ударения
				case (u_int) options_t::stress: tokenizer.setOption(tokenizer_t::options_t::stress); break;
				// Устанавливаем флаг разрешения проставлять регистры букв в словах
				case (u_int) options_t::uppers: tokenizer.setOption(tokenizer_t::options_t::uppers); break;
				// Устанавливаем флаг разрешения сборку суффиксов цифровых аббревиатур
				case (u_int) options_t::collect: tokenizer.setOption(tokenizer_t::options_t::collect); break;
				// Устанавливаем флаг разрешающий использовать фильтр Блума
				case (u_int) options_t::bloom: (almV2 ? dict2.setOption(dict_t::options_t::bloom) : dict1.setOption(dict_t::options_t::bloom)); break;
				// Устанавливаем флаг ктивации стемминга
				case (u_int) options_t::stemming: (almV2 ? dict2.setOption(dict_t::options_t::stemming) : dict1.setOption(dict_t::options_t::stemming)); break;
				// Устанавливаем флаг исправления только опечаток
				case (u_int) options_t::onlytypos: (almV2 ? dict2.setOption(dict_t::options_t::onlytypos) : dict1.setOption(dict_t::options_t::onlytypos)); break;
				// Устанавливаем флаг использования только слов из белого списка
				case (u_int) options_t::onlyGood: {
					// Устанавливаем флаг использования только слов из белого списка
					toolkit.setOption(toolkit_t::options_t::onlyGood);
					// Устанавливаем флаг использования только слов из белого списка, для языковой модели
					(almV2 ? alm2->setOption(alm_t::options_t::onlyGood) : alm1->setOption(alm_t::options_t::onlyGood));
				} break;
				// Устанавливаем флаг разрешающий детектировать слова из смешанных словарей
				case (u_int) options_t::mixdicts: {
					// Устанавливаем флаг разрешающий детектировать слова из смешанных словарей
					toolkit.setOption(toolkit_t::options_t::mixdicts);
					// Устанавливаем флаг разрешающий детектировать слова из смешанных словарей, для языковой модели
					(almV2 ? alm2->setOption(alm_t::options_t::mixdicts) : alm1->setOption(alm_t::options_t::mixdicts));
				 } break;
				// Устанавливаем флаг разрешающий загружать n-граммы из arpa так-как они есть
				case (u_int) options_t::confidence: {
					// Устанавливаем флаг разрешающий загружать n-граммы из arpa так-как они есть
					toolkit.setOption(toolkit_t::options_t::confidence);
					// Устанавливаем флаг разрешающий загружать n-граммы из arpa так-как они есть, для языковой модели
					(almV2 ? alm2->setOption(alm_t::options_t::confidence) : alm1->setOption(alm_t::options_t::confidence));
				 } break;
				 // Устанавливаем флаг разрешения использовать токен неизвестного слова
				case (u_int) options_t::allowUnk: toolkit.setOption(toolkit_t::options_t::allowUnk); break;
				// Устанавливаем флаг разрешения сбрасывать частоту токена неизвестного слова
				case (u_int) options_t::resetUnk: toolkit.setOption(toolkit_t::options_t::resetUnk); break;
				// Устанавливаем флаг разрешения использовать абсолютно все полученные n-граммы
				case (u_int) options_t::allGrams: toolkit.setOption(toolkit_t::options_t::allGrams); break;
				// Устанавливаем флаг разрешения переводить слова в нижний регистр
				case (u_int) options_t::lowerCase: toolkit.setOption(toolkit_t::options_t::lowerCase); break;
				// Устанавливаем флаг учитывающий при сборке N-грамм, только те токены, которые соответствуют словам
				case (u_int) options_t::tokenWords: toolkit.setOption(toolkit_t::options_t::tokenWords); break;
				// Устанавливаем флаг разрешения выполнять интерполяцию при расчёте arpa
				case (u_int) options_t::interpolate: toolkit.setOption(toolkit_t::options_t::interpolate); break;
				// Устанавливаем флаг режима разрешения выполнять сплитов текста
				case (u_int) options_t::ascsplit: options = spell1.setOption(spell_t::options_t::split, options); break;
				// Устанавливаем флаг разрешения на исправление слов с альтернативными буквами
				case (u_int) options_t::ascalter: options = spell1.setOption(spell_t::options_t::alter, options); break;
				// Устанавливаем флаг разрешения использовать сплиты с ошибками
				case (u_int) options_t::ascesplit: options = spell1.setOption(spell_t::options_t::esplit, options); break;
				// Устанавливаем флаг разрешения на удаление сплитов в словах
				case (u_int) options_t::ascrsplit: options = spell1.setOption(spell_t::options_t::rsplit, options); break;
				// Устанавливаем флаг разрешения проставлять регистры в словах
				case (u_int) options_t::ascuppers: options = spell1.setOption(spell_t::options_t::uppers, options); break;
				// Устанавливаем флаг разрешения выполнять сплиты по дефисам
				case (u_int) options_t::aschyphen: options = spell1.setOption(spell_t::options_t::hyphen, options); break;
				// Устанавливаем флаг пропуска слов в верхнем регистре
				case (u_int) options_t::ascskipupp: options = spell1.setOption(spell_t::options_t::skipupp, options); break;
				// Устанавливаем флаг пропуска слов с латинскими символами
				case (u_int) options_t::ascskiplat: options = spell1.setOption(spell_t::options_t::skiplat, options); break;
				// Устанавливаем флаг пропуска слова с дефисами
				case (u_int) options_t::ascskiphyp: options = spell1.setOption(spell_t::options_t::skiphyp, options); break;
				// Устанавливаем флаг удаления повторяющиеся одинаковых слов
				case (u_int) options_t::ascwordrep: options = spell1.setOption(spell_t::options_t::wordrep, options); break;
			}
		}
		/**
		 * unsetOption Метод отключения опции модуля
		 * @param option опция для отключения
		 */
		void unsetOption(const options_t option) noexcept {
			// Выполняем отключение нужный нам тип настроек
			switch((u_short) option){
				// Если включён режим отладки
				case (u_short) options_t::debug: {
					// Выполняем отключение режима отладки
					toolkit.unsetOption(toolkit_t::options_t::debug);
					// Выполняем отключение режима отладки для токенизатора
					tokenizer.unsetOption(tokenizer_t::options_t::debug);
					// Выполняем отключение режима отладки для спеллчекера
					options = spell1.unsetOption(spell_t::options_t::debug, options);
					// Выполняем отключение режима отладки языковой модели
					(almV2 ? alm2->unsetOption(alm_t::options_t::debug) : alm1->unsetOption(alm_t::options_t::debug));
					// Выполняем отключение режима отладки словаря
					(almV2 ? dict2.unsetOption(dict_t::options_t::debug) : dict1.unsetOption(dict_t::options_t::debug));
				} break;
				// Выполняем отключение флага разрешения использовать символы ударения
				case (u_int) options_t::stress: tokenizer.unsetOption(tokenizer_t::options_t::stress); break;
				// Выполняем отключение флага разрешения проставлять регистры букв в словах
				case (u_int) options_t::uppers: tokenizer.unsetOption(tokenizer_t::options_t::uppers); break;
				// Выполняем отключение флага разрешения сборку суффиксов цифровых аббревиатур
				case (u_int) options_t::collect: tokenizer.unsetOption(tokenizer_t::options_t::collect); break;
				// Выполняем отключение флага разрешающий использовать фильтр Блума
				case (u_int) options_t::bloom: (almV2 ? dict2.unsetOption(dict_t::options_t::bloom) : dict1.unsetOption(dict_t::options_t::bloom)); break;
				// Выполняем отключение флага ктивации стемминга
				case (u_int) options_t::stemming: (almV2 ? dict2.unsetOption(dict_t::options_t::stemming) : dict1.unsetOption(dict_t::options_t::stemming)); break;
				// Выполняем отключение флага исправления только опечаток
				case (u_int) options_t::onlytypos: (almV2 ? dict2.unsetOption(dict_t::options_t::onlytypos) : dict1.unsetOption(dict_t::options_t::onlytypos)); break;
				// Выполняем отключение флага использования только слов из белого списка
				case (u_int) options_t::onlyGood: {
					// Выполняем отключение флага использования только слов из белого списка
					toolkit.unsetOption(toolkit_t::options_t::onlyGood);
					// Выполняем отключение флага использования только слов из белого списка, для языковой модели
					(almV2 ? alm2->unsetOption(alm_t::options_t::onlyGood) : alm1->unsetOption(alm_t::options_t::onlyGood));
				} break;
				// Выполняем отключение флага разрешающий детектировать слова из смешанных словарей
				case (u_int) options_t::mixdicts: {
					// Выполняем отключение флага разрешающий детектировать слова из смешанных словарей
					toolkit.unsetOption(toolkit_t::options_t::mixdicts);
					// Выполняем отключение флага разрешающий детектировать слова из смешанных словарей, для языковой модели
					(almV2 ? alm2->unsetOption(alm_t::options_t::mixdicts) : alm1->unsetOption(alm_t::options_t::mixdicts));
				 } break;
				// Выполняем отключение флага разрешающий загружать n-граммы из arpa так-как они есть
				case (u_int) options_t::confidence: {
					// Выполняем отключение флага разрешающий загружать n-граммы из arpa так-как они есть
					toolkit.setOption(toolkit_t::options_t::confidence);
					// Выполняем отключение флага разрешающий загружать n-граммы из arpa так-как они есть, для языковой модели
					(almV2 ? alm2->unsetOption(alm_t::options_t::confidence) : alm1->unsetOption(alm_t::options_t::confidence));
				 } break;
				 // Выполняем отключение флага разрешения использовать токен неизвестного слова
				case (u_int) options_t::allowUnk: toolkit.unsetOption(toolkit_t::options_t::allowUnk); break;
				// Выполняем отключение флага разрешения сбрасывать частоту токена неизвестного слова
				case (u_int) options_t::resetUnk: toolkit.unsetOption(toolkit_t::options_t::resetUnk); break;
				// Выполняем отключение флага разрешения использовать абсолютно все полученные n-граммы
				case (u_int) options_t::allGrams: toolkit.unsetOption(toolkit_t::options_t::allGrams); break;
				// Выполняем отключение флага разрешения переводить слова в нижний регистр
				case (u_int) options_t::lowerCase: toolkit.unsetOption(toolkit_t::options_t::lowerCase); break;
				// Выполняем отключение флага учитывающий при сборке N-грамм, только те токены, которые соответствуют словам
				case (u_int) options_t::tokenWords: toolkit.unsetOption(toolkit_t::options_t::tokenWords); break;
				// Выполняем отключение флага разрешения выполнять интерполяцию при расчёте arpa
				case (u_int) options_t::interpolate: toolkit.unsetOption(toolkit_t::options_t::interpolate); break;
				// Выполняем отключение флага режима разрешения выполнять сплитов текста
				case (u_int) options_t::ascsplit: options = spell1.unsetOption(spell_t::options_t::split, options); break;
				// Выполняем отключение флага разрешения на исправление слов с альтернативными буквами
				case (u_int) options_t::ascalter: options = spell1.unsetOption(spell_t::options_t::alter, options); break;
				// Выполняем отключение флага разрешения использовать сплиты с ошибками
				case (u_int) options_t::ascesplit: options = spell1.unsetOption(spell_t::options_t::esplit, options); break;
				// Выполняем отключение флага разрешения на удаление сплитов в словах
				case (u_int) options_t::ascrsplit: options = spell1.unsetOption(spell_t::options_t::rsplit, options); break;
				// Выполняем отключение флага разрешения проставлять регистры в словах
				case (u_int) options_t::ascuppers: options = spell1.unsetOption(spell_t::options_t::uppers, options); break;
				// Выполняем отключение флага разрешения выполнять сплиты по дефисам
				case (u_int) options_t::aschyphen: options = spell1.unsetOption(spell_t::options_t::hyphen, options); break;
				// Выполняем отключение флага пропуска слов в верхнем регистре
				case (u_int) options_t::ascskipupp: options = spell1.unsetOption(spell_t::options_t::skipupp, options); break;
				// Выполняем отключение флага пропуска слов с латинскими символами
				case (u_int) options_t::ascskiplat: options = spell1.unsetOption(spell_t::options_t::skiplat, options); break;
				// Выполняем отключение флага пропуска слова с дефисами
				case (u_int) options_t::ascskiphyp: options = spell1.unsetOption(spell_t::options_t::skiphyp, options); break;
				// Выполняем отключение флага удаления повторяющиеся одинаковых слов
				case (u_int) options_t::ascwordrep: options = spell1.unsetOption(spell_t::options_t::wordrep, options); break;
			}
		}
		/**
		 * setSubstitutes Метод установки букв для исправления слов из смешанных алфавитов
		 * @param letters список букв разных алфавитов соответствующих друг-другу
		 */
		void setSubstitutes(const map <string, string> & letters) noexcept {
			// Устанавливаем собранные буквы
			if(!letters.empty()) alphabet.setSubstitutes(letters);
		}
		/**
		 * setZone Метод установки пользовательской зоны
		 * @param zone пользовательская зона
		 */
		void setZone(const wstring & zone) noexcept {
			// Устанавливаем доменную зону
			alphabet.setzone(zone);
		}
		/**
		 * addAbbr Метод добавления аббревиатуры
		 * @param idw идентификатор слова для добавления
		 */
		void addAbbr(const size_t idw) noexcept {
			// Добавляем аббревиатуру
			tokenizer.addAbbr(idw);
		}
		/**
		 * addAbbr Метод добавления аббревиатуры
		 * @param word слово для добавления
		 */
		void addAbbr(const wstring & word) noexcept {
			// Добавляем аббревиатуру
			tokenizer.addAbbr(word);
		}
		/**
		 * setAbbrs Метод установки списка аббревиатур
		 * @param abbrs список аббревиатур
		 */
		void setAbbrs(const set <size_t> & abbrs) noexcept {
			// Устанавливаем список аббревиатур
			tokenizer.setAbbrs(abbrs);
		}
		/**
		 * addSuffix Метод установки суффикса цифровой аббревиатуры
		 * @param idw идентификатор суффикса цифровой аббревиатуры
		 */
		void addSuffix(const size_t idw) noexcept {
			// Устанавливаем идентификатор суффикса цифровой аббревиатуры
			tokenizer.addSuffix(idw);
		}
		/**
		 * setSuffixes Метод установки списка суффиксов цифровых аббревиатур
		 * @param suffix список суффиксов цифровых аббревиатур
		 */
		void setSuffixes(const set <size_t> & suffix) noexcept {
			// Устанавливаем список суффиксов цифровых аббревиатур
			tokenizer.setSuffixes(suffix);
		}
		/**
		 * addSuffix Метод извлечения суффикса из цифровой аббревиатуры
		 * @param word слово для извлечения суффикса аббревиатуры
		 * @param idw  идентификатор обрабатываемого слова
		 */
		void addSuffix(const wstring & word, const size_t idw = idw_t::NIDW) noexcept {
			// Устанавливаем суффикс цифровой аббревиатуры
			tokenizer.addSuffix(word, idw);
		}
		/**
		 * setThreads Метод установки количества потоков
		 * @param count количество потоков для работы
		 */
		void setThreads(const size_t count = 0) noexcept {
			// Запоминаем количество потоков
			threads = count;
			// Выполняем установку количества потоков
			(almV2 ? alm2->setThreads(threads) : alm1->setThreads(threads));
			// Выполняем установку количества потоков
			(almV2 ? dict2.setThreads(threads) : dict1.setThreads(threads));
		}
		/**
		 * setAllTokenUnknown Метод установки всех токенов идентифицируемых как <unk>
		 */
		void setAllTokenUnknown() noexcept {
			// Выполняем установку всех токенов идентифицируемых как <unk>
			toolkit.setAllTokenUnknown();
			// Выполняем установку всех токенов идентифицируемых как <unk>, для языковой модели
			(almV2 ? alm2->setAllTokenUnknown() : alm1->setAllTokenUnknown());
		}
		/**
		 * setAllTokenDisable Метод установки всех токенов как не идентифицируемых
		 */
		void setAllTokenDisable() noexcept {
			// Выполняем установку всех токенов как не идентифицируемых
			toolkit.setAllTokenDisable();
			// Выполняем установку всех токенов как не идентифицируемых, для языковой модели
			(almV2 ? alm2->setAllTokenDisable() : alm1->setAllTokenDisable());
		}
		/**
		 * setUnknown Метод установки неизвестного слова
		 * @param word слово для добавления
		 */
		void setUnknown(const wstring & word) noexcept {
			// Выполняем установку неизвестного слова
			toolkit.setUnknown(alphabet.convert(word));
			// Выполняем установку неизвестного слова, для языковой модели
			(almV2 ? alm2->setUnknown(alphabet.convert(word)) : alm1->setUnknown(alphabet.convert(word)));
		}
		/**
		 * setTokenUnknown Метод установки списка токенов которых нужно идентифицировать как <unk>
		 * @param options список токенов которых нужно идентифицировать как <unk>
		 */
		void setTokenUnknown(const wstring & options) noexcept {
			// Выполняем установку списка токенов которых нужно идентифицировать как <unk>
			toolkit.setTokenUnknown(alphabet.convert(options));
			// Выполняем установку списка токенов которых нужно идентифицировать как <unk>, для языковой модели
			(almV2 ? alm2->setTokenUnknown(alphabet.convert(options)) : alm1->setTokenUnknown(alphabet.convert(options)));
		}
		/**
		 * setTokenDisable Метод установки списка не идентифицируемых токенов
		 * @param options список не идентифицируемых токенов
		 */
		void setTokenDisable(const wstring & options) noexcept {
			// Выполняем установку списка не идентифицируемых токенов
			toolkit.setTokenDisable(alphabet.convert(options));
			// Выполняем установку списка не идентифицируемых токенов, для языковой модели
			(almV2 ? alm2->setTokenDisable(alphabet.convert(options)) : alm1->setTokenDisable(alphabet.convert(options)));
		}
		/**
		 * setTokensUnknown Метод установки списка токенов приводимых к <unk>
		 * @param tokens список токенов для установки
		 */
		void setTokensUnknown(const set <size_t> & tokens) noexcept {
			// Если токены переданы
			if(!tokens.empty()){
				// Сприсок токенов
				set <token_t> tmp;
				// Переходим по всему списку токенов
				for(auto & token : tokens) tmp.emplace(token_t(token));
				// Выполняем установку списка токенов приводимых к <unk>
				toolkit.setTokensUnknown(tmp);
				// Выполняем установку списка токенов приводимых к <unk>, для языковой модели
				(almV2 ? alm2->setTokensUnknown(tmp) : alm1->setTokensUnknown(tmp));
			}
		}
		/**
		 * setTokensDisable Метод установки списка запрещённых токенов
		 * @param tokens список токенов для установки
		 */
		void setTokensDisable(const set <size_t> & tokens) noexcept {
			// Если токены переданы
			if(!tokens.empty()){
				// Сприсок токенов
				set <token_t> tmp;
				// Переходим по всему списку токенов
				for(auto & token : tokens) tmp.emplace(token_t(token));
				// Выполняем установку списка запрещённых токенов
				toolkit.setTokensDisable(tmp);
				// Выполняем установку списка запрещённых токенов, для языковой модели
				(almV2 ? alm2->setTokensDisable(tmp) : alm1->setTokensDisable(tmp));
			}
		}
		/**
		 * addBadword Метод добавления идентификатора похого слова в список
		 * @param idw идентификатор слова
		 */
		void addBadword(const size_t idw) noexcept {
			// Выполняем добавление идентификатора похого слова в список
			toolkit.addBadword(idw);
			// Выполняем добавление идентификатора похого слова в список
			(almV2 ? alm2->addBadword(idw) : alm1->addBadword(idw));
		}
		/**
		 * addBadword Метод добавления похого слова в список
		 * @param word слово для добавления
		 */
		void addBadword(const wstring & word) noexcept {
			// Выполняем добавление похого слова в список
			toolkit.addBadword(alphabet.convert(word));
			// Выполняем добавление похого слова в список
			(almV2 ? alm2->addBadword(alphabet.convert(word)) : alm1->addBadword(alphabet.convert(word)));
		}
		/**
		 * addGoodword Метод добавления идентификатора хорошего слова в список
		 * @param idw идентификатор слова
		 */
		void addGoodword(const size_t idw) noexcept {
			// Выполняем добавление идентификатора хорошего слова в список
			toolkit.addGoodword(idw);
			// Выполняем добавление идентификатора хорошего слова в список
			(almV2 ? alm2->addGoodword(idw) : alm1->addGoodword(idw));
		}
		/**
		 * addGoodword Метод добавления хорошего слова в список
		 * @param word слово для добавления
		 */
		void addGoodword(const wstring & word) noexcept {
			// Выполняем добавление хорошего слова в список
			toolkit.addGoodword(alphabet.convert(word));
			// Выполняем добавление хорошего слова в список
			(almV2 ? alm2->addGoodword(alphabet.convert(word)) : alm1->addGoodword(alphabet.convert(word)));
		}
		/**
		 * setBadwords Метод установки списка идентификаторов плохих слов в список
		 * @param idws список идентификаторов плохих слов
		 */
		void setBadwords(const set <size_t> & idws) noexcept {
			// Выполняем установку списка идентификаторов плохих слов в список
			toolkit.setBadwords(idws);
			// Выполняем установку списка идентификаторов плохих слов в список, для языковой модели
			(almV2 ? alm2->setBadwords(idws) : alm1->setBadwords(idws));
		}
		/**
		 * setBadwords Метод установки списка плохих слов в список
		 * @param badwords список плохих слов
		 */
		void setBadwords(const vector <wstring> & badwords) noexcept {
			// Список плохих слов
			vector <string> tmp;
			// Формируем новый список
			for(auto & word : badwords) tmp.push_back(alphabet.convert(word));
			// Выполняем установку списка плохих слов в список
			toolkit.setBadwords(tmp);
			// Выполняем установку списка плохих слов в список, для языковой модели
			(almV2 ? alm2->setBadwords(tmp) : alm1->setBadwords(tmp));
		}
		/**
		 * setGoodwords Метод установки списка идентификаторов хороших слов в список
		 * @param idws список идентификаторов хороших слов
		 */
		void setGoodwords(const set <size_t> & idws) noexcept {
			// Выполняем установку списка идентификаторов хороших слов в список
			toolkit.setGoodwords(idws);
			// Выполняем установку списка идентификаторов хороших слов в список, для языковой модели
			(almV2 ? alm2->setGoodwords(idws) : alm1->setGoodwords(idws));
		}
		/**
		 * setGoodwords Метод установки списка хороших слов в список
		 * @param goodwords список хороших слов
		 */
		void setGoodwords(const vector <wstring> & goodwords) noexcept {
			// Список хороших слов
			vector <string> tmp;
			// Формируем новый список
			for(auto & word : goodwords) tmp.push_back(alphabet.convert(word));
			// Выполняем установку списка хороших слов в список
			toolkit.setGoodwords(tmp);
			// Выполняем установку списка хороших слов в список, для языковой модели
			(almV2 ? alm2->setGoodwords(tmp) : alm1->setGoodwords(tmp));
		}
		/**
		 * setPilots Метод установки пилотных слов
		 * @param pilots пилотные слова для установки
		 */
		void setPilots(const vector <wstring> & pilots) noexcept {
			// Если пилотные слова получены
			if(!pilots.empty()){
				// Переходим по всему списку пилотных слов
				for(auto & word : pilots){
					// Добавляем пилотное слово
					if(!word.empty()) (almV2 ? dict2.setPilot(word.front()) : dict1.setPilot(word.front()));
				}
			}
		}
		/**
		 * addLemma Метод добавления леммы в словарь
		 * @param lemma лемма для добавления
		 */
		void addLemma(const wstring & lemma) noexcept {
			// Устанавливаем лемму
			(almV2 ? dict2.addLemma(lemma) : dict1.addLemma(lemma));
		}
		/**
		 * addAlt Метод добавления слова с альтернативной буквой
		 * @param word    слово для добавления
		 * @param alt     альтернативное слово для добавления
		 * @param context слово является контексто-зависимым
		 */
		void addAlt(const string & word, const string & alt, const bool context = false) noexcept {
			// Если слова переданы
			if(!word.empty() && !alt.empty() && (word.length() == alt.length())){
				// Выполняем конвертирование слов
				const wstring & wrd1 = alphabet.convert(word);
				const wstring & wrd2 = alphabet.convert(alt);
				// Если - это буквы
				if((wrd1.length() == 1) && (wrd2.length() == 1)){
					// Запоминаем устанавливаемые альтернативные буквы
					altLetters.emplace(wrd1.front(), wrd2.front());
					// Добавляем альтернативную букву
					(almV2 ? dict2.addAlt(wrd1.front(), wrd2.front()) : dict1.addAlt(wrd1.front(), wrd2.front()));
				// Если это добавление слов
				} else if((wrd1.length() > 1) && (wrd2.length() > 1)) {
					// Добавляем альтернативный вариант
					altWords.emplace(word, alt);
					// Добавляем альтернативное слово
					(almV2 ? dict2.addAlt(wrd1, wrd2, context) : dict1.addAlt(wrd1, wrd2, context));
				}
			}
		}
		/**
		 * addAlt Метод добавления слова с альтернативной буквой
		 * @param word    слово для добавления
		 * @param idw     идентификатор слова если есть
		 * @param context слово является контексто-зависимым
		 */
		void addAlt(const wstring & word, const size_t idw = idw_t::NIDW, const bool context = false) noexcept {
			// Добавляем альтернативное слово
			(almV2 ? dict2.addAlt(word, idw, context) : dict1.addAlt(word, idw, context));
		}
		/**
		 * addUWord Метод добавления слова, которое всегда начинается с заглавной буквы
		 * @param word слово для добавления
		 */
		void addUWord(const wstring & word) noexcept {
			// Добавляем слово с заглавной буквы в словарь
			(almV2 ? dict2.addUWord(word) : dict1.addUWord(word));
		}
		/**
		 * addUWord Метод добавления идентификатора слова, которое всегда начинается с заглавной буквы
		 * @param idw идентификатор слова для добавления
		 * @param ups регистры добавляемого слова
		 */
		void addUWord(const size_t idw, const size_t ups) noexcept {
			// Добавляем слово с заглавной буквы в словарь
			(almV2 ? dict2.addUWord(idw, ups) : dict1.addUWord(idw, ups));
		}
		/**
		 * setUWords Метод добавления списка идентификаторов слов, которые всегда начинаются с заглавной буквы
		 * @param words список идентификаторов слов для добавления
		 */
		void setUWords(const map <size_t, size_t> & words) noexcept {
			// Добавляем слово с заглавной буквы в словарь
			(almV2 ? dict2.setUWords(words) : dict1.setUWords(words));
		}
		/**
		 * setEmbedding Метод установки эмбеддинга
		 * @param embedding эмбеддинг словаря
		 * @param size      размер эмбеддинга
		 */
		void setEmbedding(const map <string, u_short> & embedding, const u_short size) noexcept {
			// Если эмбеддинг передан
			if(!embedding.empty()){
				// Выполняем создание эмбеддинга
				json emb(embedding);
				// Устанавливаем эмбеддинг
				(almV2 ? dict2.setEmbedding(emb, size) : dict1.setEmbedding(emb, size));
			}
		}
		/**
		 * generateEmbedding Метод генерации эмбеддинга
		 */
		void generateEmbedding() noexcept {
			// Выполняем генерацию эмбеддинга
			(almV2 ? dict2.generateEmbedding() : dict1.generateEmbedding());
		}
		/**
		 * setSizeEmbedding Метод установки размера эмбеддинга
		 * @param size размер эмбеддинга
		 */
		void setSizeEmbedding(const u_short size = 0) noexcept {
			// Выполняем установку размера Эмбеддинга
			(almV2 ? dict2.setSizeEmbedding(size) : dict1.setSizeEmbedding(size));
		}
		/**
		 * setAdCw Метод установки характеристик словаря
		 * @param cw количество обработанных слов
		 * @param ad количество обработанных документов
		 */
		void setAdCw(const size_t cw = 1, const size_t ad = 1) noexcept {
			// Загружаем в ALMv2
			if(almV2) dict2.setAdCw(cw, ad);
			// Загружаем в ALMv1
			else dict1.setAdCw(cw, ad);
		}
		/**
		 * setCode Метод установки кода языка
		 * @param code код языка словаря для установки
		 */
		void setCode(const wstring & code) noexcept {
			// Устанавливаем код языка
			(almV2 ? dict2.setCode(code) : dict1.setCode(code));
		}
		/**
		 * setName Метод установки названия словаря
		 * @param name название словаря
		 */
		void setName(const wstring & name) noexcept {
			// Устанавливаем название словаря
			(almV2 ? dict2.setName(name) : dict1.setName(name));
		}
		/**
		 * setAuthor Метод установки автора словаря
		 * @param author автор словаря
		 */
		void setAuthor(const wstring & author) noexcept {
			// Устанавливаем автора словаря
			(almV2 ? dict2.setAuthor(author) : dict1.setAuthor(author));
		}
		/**
		 * setLictype Метод установки типа лицензионной информации словаря
		 * @param type тип лицензионного соглашения
		 */
		void setLictype(const wstring & type) noexcept {
			// Устанавливаем тип лицензии словаря
			(almV2 ? dict2.setLictype(type) : dict1.setLictype(type));
		}
		/**
		 * setLictext Метод установки лицензионной информации словаря
		 * @param license лицензионная информация словаря
		 */
		void setLictext(const wstring & license) noexcept {
			// Устанавливаем текст лицензии словаря
			(almV2 ? dict2.setLictext(license) : dict1.setLictext(license));
		}
		/**
		 * setContacts Метод установки контактных данных автора словаря
		 * @param contacts контактные данные автора словаря
		 */
		void setContacts(const wstring & contacts) noexcept {
			// Устанавливаем контакты автора словаря
			(almV2 ? dict2.setContacts(contacts) : dict1.setContacts(contacts));
		}
		/**
		 * setCopyright Метод установки авторских прав на словарь
		 * @param copyright авторские права на словарь
		 */
		void setCopyright(const wstring & copyright) noexcept {
			// Устанавливаем копирайт автора словаря
			(almV2 ? dict2.setCopyright(copyright) : dict1.setCopyright(copyright));
		}
		/**
		 * addText Метод добавления текста для расчёта
		 * @param text текст который нужно добавить
		 * @param idd  идентификатор документа
		 */
		void addText(const string & text, const size_t idd = 0) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Добавляем текст для расчёта
				if(!text.empty()) toolkit.addText(text, idd);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * setOOvFile Метод установки файла для сохранения OOV слов
		 * @param oovfile адрес файла для сохранения oov слов
		 */
		void setOOvFile(const wstring & oovfile) noexcept {
			// Выполняем установку файла для сохранения OOV слов
			if(!oovfile.empty()) (almV2 ? alm2->setOOvFile(alphabet.convert(oovfile).c_str()) : alm1->setOOvFile(alphabet.convert(oovfile).c_str()));
		}
		/**
		 * setNSWLibCount Метод установки максимального количества вариантов для анализа
		 * @param count максимальное количество вариантов для анализа
		 */
		void setNSWLibCount(const size_t count = 0) noexcept {
			// Устанавливаем в ALMv2
			if(almV2) dict2.setNSWLibCount(count);
			// Устанавливаем в ALMv1
			else dict1.setNSWLibCount(count);
		}
		/**
		 * setUserToken Метод добавления токена пользователя
		 * @param name слово - обозначение токена
		 */
		void setUserToken(const string & name) noexcept {
			// Добавляем пользовательский токен
			toolkit.setUserToken(name);
			// Выполняем добавление токена пользователя
			(almV2 ? alm2->setUserToken(name) : alm1->setUserToken(name));
		}
		/**
		 * setStemmingMethod Метод установки функции получения леммы
		 * @param fn функция для установки
		 */
		void setStemmingMethod(stemmer_t::stemming_t fn) noexcept {
			// Если функция передана, устанавливаем её
			if(fn != nullptr) (almV2 ? dict2.setLMethod(fn) : dict1.setLMethod(fn));
		}
		/**
		 * setVariantsMethod Метод установки функции подбора вариантов
		 * @param fn функция для установки
		 */
		void setVariantsMethod(stemmer_t::variants_t fn) noexcept {
			// Если функция передана, устанавливаем её
			if(fn != nullptr) (almV2 ? dict2.setVMethod(fn) : dict1.setVMethod(fn));
		}
		/**
		 * addWord Метод добавления слова в словарь
		 * @param word слово для добавления
		 * @param idw  идентификатор слова, если нужно
		 * @param idd  идентификатор документа
		 */
		void addWord(const wstring & word, const size_t idw = 0, const size_t idd = 0) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Добавляем слово в словарь
				if(!word.empty()) toolkit.addWord(word, idw, idd);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * setWordPreprocessingMethod Метод установки функции препроцессинга слова
		 * @param fn внешняя функция препроцессинга слова
		 */
		void setWordPreprocessingMethod(function <const string (const string &, const vector <string> &)> fn) noexcept {
			// Устанавливаем функцию
			toolkit.setWordPreprocessingMethod(fn);
			// Устанавливаем функцию в языковую модель
			(almV2 ? alm2->setWordPreprocessingMethod(fn) : alm1->setWordPreprocessingMethod(fn));
		}
		/**
		 * setUserTokenMethod Метод установки функции обработки пользовательского токена
		 * @param name слово - обозначение токена
		 * @param fn   внешняя функция обрабатывающая пользовательский токен
		 */
		void setUserTokenMethod(const wstring & name, function <const bool (const string &, const string &)> fn) noexcept {
			// Выполняем добавление функции обработки пользовательского токена
			toolkit.setUserTokenMethod(alphabet.convert(name), fn);
			// Выполняем добавление функции обработки пользовательского токена в языковую модель
			(almV2 ? alm2->setUserTokenMethod(alphabet.convert(name), fn) : alm1->setUserTokenMethod(alphabet.convert(name), fn));
		}
		/**
		 * infoIndex Метод вывода информации о словаре
		 * @param filename адрес файла бинарного контейнера
		 */
		void infoIndex(const string & filename) noexcept {
			// Адрес файла для загрузки
			if(!filename.empty()){
				// Объект бинарного контейнера
				ascb_t ascb(filename, "", (!logfile.empty() ? logfile.c_str() : nullptr));
				// Устанавливаем тип языковой модели
				ascb.setALMvType(almV2);
				// Устанавливаем алфавит
				ascb.setAlphabet(&alphabet);
				// Устанавливаем токенизатор
				ascb.setTokenizer(&tokenizer);
				// Устанавливаем словарь
				ascb.setDict(almV2 ? &dict2 : &dict1);
				// Устанавливаем языковую модель
				ascb.setAlm(almV2 ? alm2.get() : alm1.get());
				// Выполняем инициализацию контейнера
				ascb.init();
				// Выводим информацию о контейнере
				ascb.info();
			}
		}
		/**
		 * loadIndex Метод загрузки бинарного индекса
		 * @param filename адрес файла бинарного контейнера
		 * @param password пароль шифрования бинарного контейнера [если требуется]
		 * @param status   внешняя функция вывода данных прогресс-бара
		 */
		void loadIndex(const string & filename, const string & password = "", function <void (const wstring &, const u_short)> status = nullptr) noexcept {
			// Адрес файла для загрузки
			if(!filename.empty()){
				// Объект бинарного контейнера
				ascb_t ascb(filename, password, (!logfile.empty() ? logfile.c_str() : nullptr));
				// Устанавливаем тип языковой модели
				ascb.setALMvType(almV2);
				// Устанавливаем алфавит
				ascb.setAlphabet(&alphabet);
				// Устанавливаем токенизатор
				ascb.setTokenizer(&tokenizer);
				// Устанавливаем словарь
				ascb.setDict(almV2 ? &dict2 : &dict1);
				// Устанавливаем языковую модель
				ascb.setAlm(almV2 ? alm2.get() : alm1.get());
				// Устанавливаем прогресс-бар
				if(status != nullptr){
					// Устанавливаем режим отладки
					ascb.setDebug(1);
					// Устанавливаем функцию вывода статуса
					ascb.setProgressFn(status);
				}
				// Устанавливаем режим отладки
				if(generalOptions.test((u_short) options_t::debug)) ascb.setDebug(2);
				// Выполняем инициализацию контейнера
				ascb.init();
				// Выполняем чтение контейнера
				ascb.read();
			}
		}
		/**
		 * saveIndex Метод создания бинарного индекса
		 * @param filename адрес файла бинарного контейнера
		 * @param password пароль шифрования бинарного контейнера [если требуется]
		 * @param aes      размер шифрования бинарного контейнера
		 * @param status   внешняя функция вывода данных прогресс-бара
		 */
		void saveIndex(const string & filename, const string & password = "", const u_short aes = 128, function <void (const wstring &, const u_short)> status = nullptr) noexcept {
			// Адрес файла для сохранения
			if(!filename.empty()){
				// Получаем инфо-данные словаря
				auto vocabInfo = toolkit.getStatistic();
				// Устанавливаем дату словаря
				(almV2 ? dict2.setDate(time(nullptr)) : dict1.setDate(time(nullptr)));
				// Если словарь существует
				if((vocabInfo.first > 0) && (vocabInfo.second > 0)){
					// Временное слово для извлечения
					word_t tmp = L"";
					// Параметры индикаторы процесса
					size_t index = 0, actual = 0, rate = 0;
					// Устанавливаем данные словаря
					(almV2 ? dict2.setAdCw(vocabInfo.second, vocabInfo.first) : dict1.setAdCw(vocabInfo.second, vocabInfo.first));
					// Выполняем извлечение слов словаря
					toolkit.words([&](const wstring & word, const size_t idw, const size_t oc, const size_t dc, const size_t count){
						// Формируем слово
						tmp = word;
						// Устанавливаем метаданные слова
						tmp.setmeta(dc, oc);
						// Добавляем слово в словарь
						(almV2 ? dict2.add(alm2->getIdw(tmp), tmp) : dict1.add(alm1->getIdw(tmp), tmp));
						// Если нужно выводить индикатор загрузки
						if(status != nullptr){
							// Общий полученный размер данных
							index++;
							// Подсчитываем статус выполнения
							actual = u_short(index / double(count) * 100.0);
							// Если процентное соотношение изменилось
							if(rate != actual){
								// Запоминаем текущее процентное соотношение
								rate = actual;
								// Выводим индикатор загрузки
								status(L"Read words", actual);
							}
						}
						// Сообщаем, что все хорошо
						return true;
					});
					// Выполняем обучение для ALMv2
					if(almV2){
						// Выполняем обучение словаря
						dict2.train([&status](const u_short rate) noexcept {
							// Выводим индикатор загрузки
							if(status != nullptr) status(L"Train dictionary", rate);
						});
					// Выполняем обучение для ALMv1
					} else {
						// Выполняем обучение словаря
						dict1.train([&status](const u_short rate) noexcept {
							// Выводим индикатор загрузки
							if(status != nullptr) status(L"Train dictionary", rate);
						});
					}
				}
				// Если словарь получен и обучен
				if(almV2 ? !dict2.empty() : !dict1.empty()){
					// Объект бинарного контейнера
					ascb_t ascb(filename, password, (!logfile.empty() ? logfile.c_str() : nullptr));
					// Устанавливаем тип языковой модели
					ascb.setALMvType(almV2);
					// Устанавливаем локаль приложения
					ascb.setLocale(deflocale);
					// Устанавливаем алфавит
					ascb.setAlphabet(&alphabet);
					// Устанавливаем токенизатор
					ascb.setTokenizer(&tokenizer);
					// Устанавливаем словарь
					ascb.setDict(almV2 ? &dict2 : &dict1);
					// Устанавливаем языковую модель
					ascb.setAlm(almV2 ? alm2.get() : alm1.get());
					// Устанавливаем прогресс-бар
					if(status != nullptr){
						// Устанавливаем режим отладки
						ascb.setDebug(1);
						// Устанавливаем функцию вывода статуса
						ascb.setProgressFn(status);
					}
					// Устанавливаем режим отладки
					if(generalOptions.test((u_short) options_t::debug)) ascb.setDebug(2);
					// Если размер шифрования передан
					if(aes > 0){
						// Если размер шифрования получен
						switch(aes){
							// Если это 192-х битное шифрование
							case 192: ascb.setAES(aspl_t::types_t::aes192); break;
							// Если это 256-и битное шифрование
							case 256: ascb.setAES(aspl_t::types_t::aes256); break;
							// Если это 128-и битное шифрование
							default: ascb.setAES(aspl_t::types_t::aes128);
						}
					// Устанавливаем тип шифрования по умолчанию
					} else ascb.setAES(aspl_t::types_t::aes128);
					// Если список альтернативных букв существуют
					if(!altLetters.empty()){
						// Переходим по всему списку альтернативных букв
						for(auto & item : altLetters) ascb.addAlt(item.first, item.second);
						// Если список альтернативных слов загружен
						if(!altWords.empty()){
							// Переходим по всему списку альтернативных слов
							for(auto & item : altWords) ascb.addAlt(item.first, item.second);
						}
					}
					// Выполняем инициализацию контейнера
					ascb.init();
					// Выполняем запись данных в файл контейнера
					ascb.write();
				}
			}
		}
		/**
		 * readVocab Метод чтения словаря
		 * @param filename адрес файла словаря
		 * @param status   внешняя функция вывода данных прогресс-бара
		 */
		void readVocab(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если адрес файла указан
			if(!filename.empty()){
				// Выполняем загрузку файла словаря vocab для ALMv2
				if(almV2) dict2.readVocab(filename, status);
				// Выполняем загрузку файла словаря vocab для ALMv1
				else dict1.readVocab(filename, status);
			}
		}
		/**
		 * readArpa Метод чтения arpa файла, языковой модели
		 * @param filename адрес файла словаря
		 * @param status   внешняя функция вывода данных прогресс-бара
		 */
		void readArpa(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если адрес файла указан
			if(!filename.empty()){
				// Выполняем чтение arpa для ALMv2
				if(almV2) alm2->read(filename, status);
				// Выполняем чтение arpa для ALMv1
				else alm1->read(filename, status);
			}
		}
		/**
		 * writeWords Метод записи данных слов в файл
		 * @param filename адрес файла для записи
		 * @param status   функция вывода статуса записи
		 */
		void writeWords(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем запись слов из словаря в файл
				if(!filename.empty()) toolkit.writeWords(filename, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * writeVocab Метод записи данных словаря в файл
		 * @param filename адрес файла для записи
		 * @param status   функция вывода статуса записи
		 */
		void writeVocab(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем запись слов из словаря в файл
				if(!filename.empty()) toolkit.writeVocab(filename, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * writeMap Метод записи карты последовательности в файл
		 * @param filename адрес map файла карты последовательности
		 * @param status   функция вывода статуса записи
		 */
		void writeMap(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем запись карты последовательностей в файл
				if(!filename.empty()) toolkit.writeMap(filename, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * writeArpa Метод записи данных в файл arpa
		 * @param filename адрес файла для записи
		 * @param status   функция вывода статуса записи
		 */
		void writeArpa(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем запись данных ARPA в файл
				if(!filename.empty()) toolkit.writeArpa(filename, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * writeNgrams Метод записи данных в файлы ngrams
		 * @param filename адрес файла для записи
		 * @param status   функция вывода статуса записи
		 */
		void writeNgrams(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем запись N-грамм в файл
				if(!filename.empty()) toolkit.writeNgrams(filename, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * writeSuffix Метод записи данных в файл суффиксов цифровых аббревиатур
		 * @param filename адрес файла для записи
		 * @param status   функция вывода статуса
		 */
		void writeSuffix(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Выполняем запись идентификаторов цифровых аббревиатур в файл
			if(!filename.empty()) tokenizer.writeSuffix(filename, status);
		}
		/**
		 * readSuffix Метод чтения данных из файла суффиксов цифровых аббревиатур
		 * @param filename адрес файла для чтения
		 * @param status   функция вывода статуса
		 */
		void readSuffix(const string & filename, function <void (const string &, const u_short)> status = nullptr) noexcept {
			// Выполняем чтение идентификаторов цифровых аббревиатур из файла
			if(!filename.empty()) tokenizer.readSuffix(filename, status);
		}
		/**
		 * writeAbbrs Метод записи данных в файл аббревиатур
		 * @param filename адрес файла для записи
		 * @param status   функция вывода статуса
		 */
		void writeAbbrs(const string & filename, function <void (const u_short)> status = nullptr) noexcept {
			// Если адрес файла передан
			if(!filename.empty()){
				// Получаем список токенов
				const auto & tokens = tokenizer.getAbbrs();
				// Если список токенов получен
				if(!tokens.empty()){
					// Открываем файл на запись
					ofstream file(filename, ios::binary);
					// Если файл открыт, выполняем запись в файл результата
					if(file.is_open()){
						// Параметры индикаторы процесса
						size_t index = 0, actual = 0, rate = 0;
						// Переходим по всему списку токенов
						for(auto & token : tokens){
							// Создаём текст для записи
							const string & text = alphabet.format("%zu\r\n", token);
							// Выполняем запись данных в файл
							file.write(text.data(), text.size());
							// Если отладка включена
							if(status != nullptr){
								// Общий полученный размер данных
								index++;
								// Подсчитываем статус выполнения
								actual = u_short(index / double(tokens.size()) * 100.0);
								// Если процентное соотношение изменилось
								if(rate != actual){
									// Запоминаем текущее процентное соотношение
									rate = actual;
									// Отображаем ход процесса
									status(actual);
								}
							}
						}
						// Закрываем файл
						file.close();
					}
				}
			}
		}
		/**
		 * buildArpa Метод сборки ARPA
		 * @param status внешняя функция вывода данных прогресс-бара
		 */
		void buildArpa(function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем обучение
				toolkit.train(status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * buildIndex Метод сборки индекса Спеллчекера
		 * @param status внешняя функция вывода данных прогресс-бара
		 */
		void buildIndex(function <void (const u_short)> status = nullptr) noexcept {
			// Выполняем обучение для ALMv2
			if(almV2) dict2.train(status);
			// Выполняем обучение для ALMv1
			else dict1.train(status);
		}
		/**
		 * buildBloom Метод сборки фильтра Блума
		 * @param status внешняя функция вывода данных прогресс-бара
		 */
		void buildBloom(function <void (const u_short)> status = nullptr) noexcept {
			// Выполняем загрузку фильтра Блума для ALMv2
			if(almV2) dict2.bloom(status);
			// Выполняем загрузку фильтра Блума для ALMv1
			else dict1.bloom(status);
		}
		/**
		 * buildStemming Метод сборки стеммера
		 * @param status внешняя функция вывода данных прогресс-бара
		 */
		void buildStemming(function <void (const u_short)> status = nullptr) noexcept {
			// Выполняем загрузку стемминга для ALMv2
			if(almV2) dict2.stemming(status);
			// Выполняем загрузку стемминга для ALMv1
			else dict1.stemming(status);
		}
		/**
		 * pruneArpa Метод прунинга языковой модели
		 * @param threshold порог частоты прунинга
		 * @param mingram   значение минимальной n-граммы за которую нельзя прунить
		 * @param status    функция вывода статуса обучения
		 */
		void pruneArpa(const double threshold, const u_short mingram, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем прунинг
				toolkit.prune(threshold, mingram, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * pruneVocab Метод прунинга словаря
		 * @param wltf   пороговый вес слова для прунинга
		 * @param oc     встречаемость слова во всех документах
		 * @param dc     количество документов в которых встретилось слово
		 * @param status статус прунинга словаря
		 */
		void pruneVocab(const double wltf = 0.0, const size_t oc = 0, const size_t dc = 0, function <void (const u_short)> status = nullptr) noexcept {
			// Если тулкит инициализирован
			if(toolkitInit){
				// Выполняем прунинг словаря
				toolkit.pruneVocab(wltf, oc, dc, status);
			// Выводим сообщение об ошибке
			} else cerr << "Error: initialization failed" << endl;
		}
		/**
		 * word Метод извлечения слова по его идентификатору
		 * @param idw идентификатор слова
		 * @param ups регистры слова
		 * @return    слово соответствующее идентификатору
		 */
		const wstring word(const size_t idw, const size_t ups = 0) noexcept {
			// Выводим слово, если найдено
			return (almV2 ? alm2->word(idw, ups).wreal() : alm1->word(idw, ups).wreal());
		}
		/**
		 * delInText Метод очистки текста
		 * @param text текст для очистки
		 * @param flag флаг критерия очистки
		 * @return     текст без запрещенных символов
		 */
		const wstring delInText(const wstring & text, const wdel_t flag = wdel_t::broken) noexcept {
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем удаление знаков пунктуации в тексте
				case u_short(wdel_t::punct): return alphabet.delPunctInWord(text);
				// Выполняем удаление всех символов кроме разрешенных
				case u_short(wdel_t::broken): return alphabet.delBrokenInWord(text);
				// Выполняем удаление весх дефисов в тексте
				case u_short(wdel_t::hyphen): return alphabet.delHyphenInWord(text);
			}
			// Выводим результат по умолчанию
			return text;
		}
		/**
		 * check Метод проверки строки
		 * @param str  строка для проверки
		 * @param flag флаг выполняемой проверки
		 * @return     результат проверки
		 */
		const bool check(const wstring & str, const check_t flag = check_t::letter) noexcept {
			// Переводим слово в нижний регистр
			const wstring & tmp = alphabet.toLower(str);
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем проверку на Дом-2
				case u_short(check_t::home2): return alphabet.checkHome2(tmp);
				// Выполняем проверку на наличии латинского символа
				case u_short(check_t::latian): return alphabet.checkLatian(tmp);
				// Выполняем проверку на наличии дефиса
				case u_short(check_t::hyphen): return alphabet.checkHyphen(tmp);
				// Выполняем проверку легальности буквы
				case u_short(check_t::letter): return alphabet.check(tmp.front());
				// Выполняем проверку на симиляции букв с другими языками
				case u_short(check_t::similars): return alphabet.checkSimilars(tmp);
			}
			// Выводим результат по умолчанию
			return false;
		}
		/**
		 * match Метод проверки соответствия строки
		 * @param str  строка для проверки
		 * @param flag флаг типа проверки
		 * @return     результат проверки
		 */
		const bool match(const wstring & str, const match_t flag = match_t::allowed) noexcept {
			// Переводим слово в нижний регистр
			const wstring & tmp = alphabet.toLower(str);
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем проверку на соответствие слова url адресу
				case u_short(match_t::url): return alphabet.isUrl(tmp);
				// Выполняем проверку на соответствие слова аббревиатуре
				case u_short(match_t::abbr): return tokenizer.isAbbr(tmp);
				// Выполняем проверку является ли строка латиницей
				case u_short(match_t::latian): return alphabet.isLatian(tmp);
				// Выполняем проверку на соответствие слова числу
				case u_short(match_t::number): return alphabet.isNumber(tmp);
				// Выполняем проверку на соответствие слова псевдо-числу
				case u_short(match_t::anumber): return alphabet.isANumber(tmp);
				// Выполняем проверку на соответствие слова словарю
				case u_short(match_t::allowed): return alphabet.isAllowed(tmp);
				// Выполняем проверку на соответствие слова дробному числу
				case u_short(match_t::decimal): return alphabet.isDecimal(tmp);
				// Выполняем проверку на определение математических операий
				case u_short(match_t::math): return alphabet.isMath(tmp.front());
				// Выполняем проверку является ли буква символом греческого алфавита
				case u_short(match_t::greek): return alphabet.isGreek(tmp.front());
				// Выполняем проверку является ли буква символом направления (стрелки)
				case u_short(match_t::route): return alphabet.isRoute(tmp.front());
				// Выполняем проверку на символ верхнего регистра
				case u_short(match_t::upper): return alphabet.isUpper(str.front());
				// Выполняем проверку является ли буква, знаком препинания
				case u_short(match_t::punct): return alphabet.isPunct(tmp.front());
				// Выполняем проверку является ли буква пробелом
				case u_short(match_t::space): return alphabet.isSpace(tmp.front());
				// Выполняем проверку является ли буква валидной (находится ли в словаре)
				case u_short(match_t::letter): return alphabet.isLetter(tmp.front());
				// Выполняем проверку является ли буква спец-символом
				case u_short(match_t::special): return alphabet.isSpecial(tmp.front());
				// Выполняем проверку является ли буква символом игральной карты
				case u_short(match_t::pcards): return alphabet.isPlayCards(tmp.front());
				// Выполняем проверку является ли буква символом мировой валюты
				case u_short(match_t::currency): return alphabet.isCurrency(tmp.front());
				// Выполняем проверку является ли буква символом изоляции
				case u_short(match_t::isolation): return alphabet.isIsolation(tmp.front());
			}
			// Выводим результат по умолчанию
			return false;
		}
		/**
		 * idt Метод извлечения идентификатора токена
		 * @param  word слово для получения идентификатора
		 * @return      идентификатор токена
		 */
		const size_t idt(const wstring & word) noexcept {
			// Выводим идентификатор токена
			return size_t(tokenizer.idt(word));
		}
		/**
		 * ids Метод извлечения идентификатора последовательности
		 * @param  seq последовательность для получения идентификатора
		 * @return     идентификатор последовательности
		 */
		const size_t ids(const vector <size_t> & seq) noexcept {
			// Выводим идентификатор последовательности
			return tokenizer.ids(seq);
		}
		/**
		 * fti Метод удаления дробной части числа
		 * @param  num   число для обработки
		 * @param  count количество символов после запятой
		 * @return       число без дробной части
		 */
		const size_t fti(const double num, const size_t count = 0) noexcept {
			// Выполняем удаление дробной части
			return tokenizer.fti(num, count);
		}
		/**
		 * idw Метод извлечения идентификатора слова
		 * @param  word  слово для получения идентификатора
		 * @param  check нужно выполнить дополнительную проверку слова
		 * @return       идентификатор слова
		 */
		const size_t idw(const wstring & word, const bool check = true) noexcept {
			// Выводим идентификатор слова
			return (almV2 ? alm2->getIdw(word, check) : alm1->getIdw(word, check));
		}
		/**
		 * mulctLevenshtein Определение количества штрафов на основе Дамерау-Левенштейна
		 * @param  pattern шаблон с которым идет сравнение
		 * @param  text    исходный текст
		 * @return         дистанция
		 */
		const size_t mulctLevenshtein(const wstring & pattern, const wstring & text) noexcept {
			// Выводим дистанцию
			return algorithms.mulct(pattern, text);
		}
		/**
		 * damerauLevenshtein Определение дистанции Дамерау-Левенштейна в фразах
		 * @param  pattern шаблон с которым идет сравнение
		 * @param  text    исходный текст
		 * @return         дистанция
		 */
		const size_t damerauLevenshtein(const wstring & pattern, const wstring & text) noexcept {
			// Выводим дистанцию Дамерау-Левенштейна
			return algorithms.damerau(pattern, text);
		}
		/**
		 * distanceLevenshtein Определение дистанции Левенштейна в фразах
		 * @param  pattern шаблон с которым идет сравнение
		 * @param  text    исходный текст
		 * @return         дистанция
		 */
		const size_t distanceLevenshtein(const wstring & pattern, const wstring & text) noexcept {
			// Выводим дистанцию Левенштейна
			return algorithms.distance(pattern, text);
		}
		/**
		 * tanimoto Метод определения коэффициента Жаккара (частное — коэф. Танимото)
		 * @param  first  первое слово
		 * @param  second второе слово
		 * @param  stl    размер подстроки при сравнении двух слов (от 1 до минимального размера слова)
		 * @return        коэффициент Танимото
		 */
		const double tanimoto(const wstring & first, const wstring & second, const size_t stl = 2) noexcept {
			// Выводим значение Танимото
			return algorithms.tanimoto(first, second, stl);
		}
		/**
		 * needlemanWunsch Метод натяжения слов
		 * @param first    первое слово
		 * @param second   второе слово
		 * @param match    вес соответствия
		 * @param mismatch вес несоответствия
		 * @param gap      размер разрыва
		 * @return         количество очков
		 */
		const int needlemanWunsch(const wstring & first, const wstring & second, const int match = 1, const int mismatch = -1, const int gap = -2) noexcept {
			// Выводим результат натяжения
			return algorithms.needlemanWunsch(first, second, match, mismatch, gap);
		}
		/**
		 * getName Метод извлечения названия библиотеки
		 * @return название библиотеки
		 */
		const wstring getName() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_NAME);
		}
		/**
		 * getEmail Метод извлечения электронной почты автора
		 * @return электронная почта автора
		 */
		const wstring getEmail() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_EMAIL);
		}
		/**
		 * getPhone Метод извлечения телефона автора
		 * @return номер телефона автора
		 */
		const wstring getPhone() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_PHONE);
		}
		/**
		 * getAuthor Метод извлечения имени автора
		 * @return имя автора библиотеки
		 */
		const wstring getAuthor() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_AUTHOR);
		}
		/**
		 * getContact Метод извлечения контактных данных автора
		 * @return контактные данные автора
		 */
		const wstring getContact() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_CONTACT);
		}
		/**
		 * getSite Метод извлечения адреса сайта автора
		 * @return адрес сайта автора
		 */
		const wstring getSite() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_SITE);
		}
		/**
		 * getVersion Метод получения версии языковой модели
		 * @return версия языковой модели
		 */
		const wstring getVersion() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_ASC_VERSION);
		}
		/**
		 * getUnknown Метод извлечения неизвестного слова
		 * @return установленное неизвестное слово
		 */
		const wstring getUnknown() noexcept {
			// Выводим результат
			return alphabet.convert(almV2 ? alm2->getUnknown() : alm1->getUnknown());
		}
		/**
		 * getAlphabet Метод получения алфавита языка
		 * @return алфавит языка
		 */
		const wstring getAlphabet() noexcept {
			// Выводим данные алфавита
			return alphabet.convert(alphabet.get());
		}
		/**
		 * size Метод получения размера n-грамы
		 * @return длина n-граммы в языковой моделе
		 */
		const size_t size() noexcept {
			// Выводим результат
			return (almV2 ? alm2->getSize() : alm1->getSize());
		}
		/**
		 * getAbbrs Метод извлечения списка аббревиатур
		 * @return список аббревиатур
		 */
		const set <size_t> & getAbbrs() noexcept {
			// Выводим результат
			return tokenizer.getAbbrs();
		}
		/**
		 * getSuffixes Метод извлечения списка суффиксов цифровых аббревиатур
		 * @return список цифровых аббревиатур
		 */
		const set <size_t> & getSuffixes() noexcept {
			// Выводим результат
			return tokenizer.getSuffixes();
		}
		/**
		 * getUserTokenId Метод получения идентификатора пользовательского токена
		 * @param name слово для которого нужно получить идентификатор
		 * @return     идентификатор пользовательского токена соответствующий слову
		 */
		const size_t getUserTokenId(const wstring & name) noexcept {
			// Выводим результат
			return (almV2 ? alm2->getUserTokenId(alphabet.convert(name)) : alm1->getUserTokenId(alphabet.convert(name)));
		}
		/**
		 * getUserTokens Метод извлечения списка пользовательских токенов
		 * @return список пользовательских токенов
		 */
		const vector <wstring> getUserTokens() noexcept {
			// Результат работы функции
			vector <wstring> result;
			// Получаем список токенов
			const auto & tokens = (almV2 ? alm2->getUserTokens() : alm1->getUserTokens());
			// Если токены получены
			if(!tokens.empty()){
				// Переходим по списку токенов
				for(auto & token : tokens) result.push_back(alphabet.convert(token));
			}
			// Выводим результат
			return result;
		}
		/**
		 * getUppers Метод извлечения регистров для каждого слова
		 * @param seq последовательность слов для сборки контекста
		 * @return    список извлечённых последовательностей
		 */
		const vector <size_t> getUppers(const vector <size_t> & seq) noexcept {
			// Создаём список регистров
			vector <size_t> upps;
			// Выполняем извлечение регистров для каждого слова
			(almV2 ? alm2->getUppers(seq, upps) : alm1->getUppers(seq, upps));
			// Выводим список регистров
			return upps;
		}
		/**
		 * getTokensUnknown Метод извлечения списка токенов приводимых к <unk>
		 * @return список токенов
		 */
		const set <size_t> getTokensUnknown() noexcept {
			// Результат работы функции
			set <size_t> result;
			// Извлекаем список токенов
			const auto & tokens = toolkit.getTokensUnknown();
			// Если список токенов получен
			if(!tokens.empty()){
				// Переходим по всему списку токенов
				for(auto & token : tokens) result.emplace(size_t(token));
			}
			// Выводим результат
			return result;
		}
		/**
		 * getTokensDisable Метод извлечения списка запрещённых токенов
		 * @return список токенов
		 */
		const set <size_t> getTokensDisable() noexcept {
			// Результат работы функции
			set <size_t> result;
			// Извлекаем список токенов
			const auto & tokens = toolkit.getTokensDisable();
			// Если список токенов получен
			if(!tokens.empty()){
				// Переходим по всему списку токенов
				for(auto & token : tokens) result.emplace(size_t(token));
			}
			// Выводим результат
			return result;
		}
		/**
		 * getBadwords Метод извлечения чёрного списка
		 * @return чёрный список слов
		 */
		const set <size_t> & getBadwords() noexcept {
			// Выводим результат
			return toolkit.getBadwords();
		}
		/**
		 * getGoodwords Метод извлечения белого списка
		 * @return белый список слов
		 */
		const set <size_t> & getGoodwords() noexcept {
			// Выводим результат
			return toolkit.getGoodwords();
		}
		/**
		 * getSubstitutes Метод извлечения букв для исправления слов из смешанных алфавитов
		 * @param return список букв разных алфавитов соответствующих друг-другу
		 */
		const map <wstring, wstring> getSubstitutes() noexcept {
			// Результат работы функции
			map <wstring, wstring> result;
			// Получаем список букв
			const auto & letters = alphabet.getSubstitutes();
			// Если список букв получен
			if(!letters.empty()){
				// Переходим по всему списку букв
				for(auto & item : letters){
					// Формируем новый список букв
					result.emplace(
						alphabet.convert(item.first),
						alphabet.convert(item.second)
					);
				}
			}
			// Выводим результат
			return result;
		}
		/**
		 * getUserTokenWord Метод получения пользовательского токена по его идентификатору
		 * @param idw идентификатор пользовательского токена
		 * @return    пользовательский токен соответствующий идентификатору
		 */
		const wstring getUserTokenWord(const size_t idw) noexcept {
			// Выводим результат
			return alphabet.convert(almV2 ? alm2->getUserTokenWord(idw) : alm1->getUserTokenWord(idw));
		}
		/**
		 * erratum Метод поиска в тексте опечаток
		 * @param text текст в котором нужно произвести поиск
		 * @return     список с ошибочными словами в тексте
		 */
		const vector <wstring> erratum(const wstring & text) noexcept {
			// Список слов с ошибками
			vector <wstring> errors;
			// Выполняем поиск слов с ошибками
			(almV2 ? spell2.erratum(text, options, errors) : spell1.erratum(text, options, errors));
			// Выводим результат
			return errors;
		}
		/**
		 * token Метод определения типа токена слова
		 * @param word слово для которого нужно определить тип токена
		 * @return     тип токена слова
		 */
		const wstring token(const wstring & word) noexcept {
			// Результат работы функции
			wstring result = L"";
			// Если слово передано
			if(!word.empty()){
				// Выполняем получение токена слова
				const size_t idw = (almV2 ? alm2->getIdw(word) : alm1->getIdw(word));
				// Извлекаем данные слова
				const auto & token = (almV2 ? alm2->word(idw) : alm1->word(idw));
				// Если - это не токен, значит слово
				if((token.front() == L'<') && (token.back() == L'>'))
					// Выводим тип полученного токена
					result = token.wstr();
				// Сообщаем, что - это обычное слово
				else result = L"<word>";
			}
			// Выводим результат
			return result;
		}
		/**
		 * split Метод выполнения разбивку слипшихся слов
		 * @param text текст для которого нужно провести сплит
		 * @return     вариант текста с разбитыми по пробелам слов
		 */
		const wstring split(const wstring & text) noexcept {
			// Результат работы функции
			wstring result = text;
			// Если текст передан
			if(!text.empty()){
				// Список проспличенных слов
				vector <wstring> words;
				// Выполняем сплит слова
				(almV2 ? spell2.split(text, options, words) : spell1.split(text, options, words));
				// Если список слов получен, выполняем сборку контекста
				if(!words.empty()) result = tokenizer.restore(words);
			}
			// Выводим результат
			return result;
		}
		/**
		 * splitByHyphens Метод выполнения разбивку слипшихся слов по дефисам
		 * @param text текст для которого нужно провести сплит
		 * @return     вариант текста с разбитыми по пробелам слов
		 */
		const wstring splitByHyphens(const wstring & text) noexcept {
			// Результат работы функции
			wstring result = text;
			// Если текст передан
			if(!text.empty()){
				// Список последовательности
				vector <size_t> seq;
				// Список проспличенных слов
				vector <wstring> words;
				// Выполняем сплит слова
				(almV2 ? spell2.hyphen(text, options, seq, words) : spell1.hyphen(text, options, seq, words));
				// Если список слов получен, выполняем сборку контекста
				if(!words.empty()) result = tokenizer.restore(words);
			}
			// Выводим результат
			return result;
		}
		/**
		 * check Метод проверки слова на существование его в словаре
		 * @param word слово которое нужно проверить
		 * @return     результат проверки
		 */
		const bool check(const wstring & word) noexcept {
			// Результат работы функции
			bool result = false;
			// Выполняем проверку существования слова
			if(!word.empty()) result = (almV2 ? spell2.check(word) : spell1.check(word));
			// Выводим результат
			return result;
		}
		/**
		 * spell Метод выполнения исправления опечаток
		 * @param text текст в котором нужно произвести исправление
		 * @param stat флаг сбора статистики работы спеллчекера
		 * @return     исправленный текст и собранная статистика
		 */
		const pair <wstring, vector <pair <wstring, wstring>>> spell(const wstring & text, const bool stat = false) noexcept {
			// Результат работы функции
			pair <wstring, vector <pair <wstring, wstring>>> result = {text, {}};
			// Если текст передан
			if(!result.first.empty()){
				// Информационные собранные данные исправлений
				vector <vector <pair <wstring, wstring>>> info;
				// Выполняем исправление опечаток
				(almV2 ? spell2.spell(result.first, options, (stat ? &info : nullptr)) : spell1.spell(result.first, options, (stat ? &info : nullptr)));
				// Если информационный блок получен
				if(!info.empty()){
					// Переходим по всему блоку информации
					for(auto & item : info){
						// Переходим по всему списку вариантов
						for(auto & value : item){
							// Если варианты разные
							if(value.first.compare(value.second) != 0){
								// Если - это не существующий контекст
								if(value.second.compare(NOTFOUND) == 0)
									// Формируем аналитические данные
									result.second.emplace_back(value.first, L"-");
								// Если это существующих котнекст, формируем аналитические данные
								else result.second.emplace_back(value.first, value.second);
							}
						}
					}
				}
			}
			// Выводим результат
			return result;
		}
		/**
		 * analyze Метод выполнения анализа текста
		 * @param text текст в котором нужно произвести исправление
		 * @return     собранные данные анализа текста
		 */
		const vector <pair <wstring, vector <wstring>>> analyze(const wstring & text) noexcept {
			// Результат работы функции
			vector <pair <wstring, vector <wstring>>> result;
			// Если текст передан
			if(!text.empty()){
				// Информационные собранные данные аналитики
				vector <unordered_map <wstring, set <wstring>>> info;
				// Выполняем сборку данных
				(almV2 ? spell2.analyze(text, options, info) : spell1.analyze(text, options, info));
				// Если анализ получен
				if(!info.empty()){
					// Список собранных слов
					vector <wstring> words;
					// Переходим по всему списку
					for(auto & item : info){
						// Переходим по всему списку вариантов
						for(auto & value : item){
							// Очищаем список собранных слов
							words.clear();
							// Переходим по остальным вариантам
							for(auto & item : value.second){
								// Если слово не совпадает с основным словом
								if(value.first.compare(item) != 0){
									// Если - это неверный контекст
									if(item.compare(NOTFOUND) == 0)
										// Сообщаем, что контекст неверный
										words.push_back(L"-");
									// Добавляем слово в список
									else words.push_back(item);
								}
							}
							// Выводим скобку
							if(!words.empty()) result.emplace_back(value.first, move(words));
						}
					}
				}
			}
			// Выводим результат
			return result;
		}
		/**
		 * collectCorpus Метод обучения сборки текстовых данных Спеллчекера
		 * @param corpus    текстовый корпус для обучения
		 * @param smoothing тип сглаживания языковой модели
		 * @param mod       значение модификатора или дельты в зависимости от типа сглаживания
		 * @param modified  модификация количества уже изменённых младших n-грамм
		 * @param prepares  необходимость изменения граммности, после вычисления
		 * @param status    внешняя функция вывода данных прогресс-бара
		 */
		void collectCorpus(const wstring & corpus, const smoothing_t smoothing = smoothing_t::wittenBell, const double mod = 0.0, const bool modified = false, const bool prepares = false, function <void (const wstring &, const u_short)> status = nullptr) noexcept {
			// Если адрес файла корпуса передан
			if(!corpus.empty()){
				// Запоминаем, что тулкит инициализирован
				toolkitInit = true;
				// Получаем путь корпуса
				const string corpuspath = alphabet.convert(corpus);
				// Объявляем объект коллектора
				collector_t collector(&toolkit, &alphabet, &tokenizer, (!logfile.empty() ? logfile.c_str() : nullptr));
				// Устанавливаем размер n-граммы
				collector.setOrder(order);
				// Запрещаем использовать объект Python
				collector.disallowPython();
				// Устанавливаем количество потоков
				collector.setThreads(threads);
				// Устанавливаем флаг сегментации
				collector.setSegment(true, "auto");
				// Устанавливаем прогресс-бар
				if(status != nullptr){
					// Устанавливаем режим отладки
					collector.setDebug(1);
					// Устанавливаем функцию вывода статуса
					collector.setProgressFn(status);
				}
				// Устанавливаем режим отладки
				if(generalOptions.test((u_short) options_t::debug)) collector.setDebug(2);
				// Если это WittenBell
				if(smoothing == smoothing_t::wittenBell) toolkit.init(toolkit_t::algorithm_t::wittenBell, false, false, 0.0);
				// Если это AddSmooth
				else if(smoothing == smoothing_t::addSmooth) toolkit.init(toolkit_t::algorithm_t::addSmooth, false, false, mod);
				// Если это GoodTuring
				else if(smoothing == smoothing_t::goodTuring) toolkit.init(toolkit_t::algorithm_t::goodTuring, false, false, 0.0);
				// Если это ConstDiscount
				else if(smoothing == smoothing_t::constDiscount) toolkit.init(toolkit_t::algorithm_t::constDiscount, false, false, mod);
				// Если это NaturalDiscount
				else if(smoothing == smoothing_t::naturalDiscount) toolkit.init(toolkit_t::algorithm_t::naturalDiscount, false, false, 0.0);
				// Если это KneserNey
				else if(smoothing == smoothing_t::kneserNey) toolkit.init(toolkit_t::algorithm_t::kneserNey, modified, prepares, 0.0);
				// Если это ModKneserNey
				else if(smoothing == smoothing_t::modKneserNey) toolkit.init(toolkit_t::algorithm_t::modKneserNey, modified, prepares, 0.0);
				// Выполняем чтение данных каталога
				if(fsys_t::isdir(corpuspath)) collector.readDir(corpuspath, "txt");
				// Если текстовый корпус является файлом
				else if(fsys_t::isfile(corpuspath)) collector.readFile(corpuspath);
			}
		}
		/**
		 * jsonToText Метод преобразования текста в формате json в текст
		 * @param text     текст для преобразования в формате json
		 * @param callback функция обратного вызова
		 */
		void jsonToText(const wstring & text, function <void (const wstring &)> callback) noexcept {
			// Запускаем обработку конвертации
			tokenizer.jsonToText(alphabet.convert(text), [&callback](const string & chunk){
				// Выводим результат
				callback(alphabet.convert(chunk));
			});
		}
		/**
		 * textToJson Метод преобразования текста в json
		 * @param text     текст для преобразования
		 * @param callback функция обратного вызова
		 */
		void textToJson(const wstring & text, function <void (const wstring &)> callback) noexcept {
			// Запускаем обработку конвертации
			tokenizer.textToJson(alphabet.convert(text), [&callback](const string & chunk){
				// Выводим результат
				callback(alphabet.convert(chunk));
			});
		}
		/**
		 * restore Метод восстановления текста из контекста
		 * @param context токенизированный контекст
		 * @return        результирующий текст
		 */
		const wstring restore(const vector <wstring> & context) noexcept {
			// Восстанавливаем текст
			return tokenizer.restore(context);
		}
		/**
		 * context Метод сборки текстового контекста из последовательности
		 * @param seq  последовательность слов для сборки контекста
		 * @param nwrd флаг разрешающий вывод системных токенов
		 * @return     собранный текстовый контекст
		 */
		const wstring context(const vector <size_t> & seq, const bool nwrd = false) noexcept {
			// Выполняем сборку текстового контекста из последовательности
			return (almV2 ? alm2->context(seq, nwrd) : alm1->context(seq, nwrd));
		}
		/**
		 * tokenization Метод разбивки текста на токены
		 * @param text     входной текст для обработки
		 * @param callback функция обратного вызова
		 */
		void tokenization(const wstring & text, function <const bool (const wstring &, const vector <wstring> &, const bool, const bool)> callback) noexcept {
			// Контекст сконвертированный
			vector <wstring> seq;
			// Запускаем обработку токенизации
			tokenizer.run(text, [&seq, &callback](const wstring & word, const vector <string> & context, const bool reset, const bool stop){
				// Очищаем список последовательности
				seq.clear();
				// Если последовательность получена
				if(!context.empty()){
					// Переходим по всему контексту
					for(auto & word : context) seq.push_back(alphabet.convert(word));
				}
				// Выводим результат
				return callback(word, seq, reset, stop);
			});
		}
		/**
		 * urls Метод извлечения координат url адресов в строке
		 * @param text текст для извлечения url адресов
		 * @return     список координат с url адресами
		 */
		const map <size_t, size_t> urls(const wstring & text) noexcept {
			// Выводим координаты url адреса
			return alphabet.urls(text);
		}
		/**
		 * checkHypLat Метод поиска дефиса и латинского символа
		 * @param str строка для проверки
		 * @return    результат проверки
		 */
		const pair <bool, bool> checkHypLat(const wstring & str) noexcept {
			// Выводим результат првоерки
			return alphabet.checkHypLat(str);
		}
		/**
		 * countLetter Метод подсчета количества указанной буквы в слове
		 * @param word   слово в котором нужно подсчитать букву
		 * @param letter букву которую нужно подсчитать
		 * @return       результат подсчёта
		 */
		const size_t countLetter(const wstring & word, const wstring & letter) noexcept {
			// Выводим результат подсчёта
			return alphabet.countLetter(word, letter.front());
		}
		/**
		 * rest Метод исправления и детектирования слов со смешанными алфавитами
		 * @param  word слово для проверки и исправления
		 * @return      результат исправления
		 */
		const wstring rest(const wstring & word) noexcept {
			// Создаем слово для исправления
			wstring result = alphabet.toLower(word);
			// Выполняем исправление слов
			alphabet.rest(result);
			// Выводим результат
			return result;
		}
		/**
		 * fixUppers Метод исправления регистров в тексте
		 * @param text текст для исправления регистров
		 * @return     текст с исправленными регистрами слов
		 */
		const wstring fixUppers(const wstring & text) noexcept {
			// Выполняем исправление регистров в тексте
			return (almV2 ? alm2->fixUppers(text) : alm1->fixUppers(text));
		}
		/**
		 * perplexity Метод расчёта перплексии текста
		 * @param  text текст для расчёта
		 * @return      результат расчёта
		 */
		const alm_t::ppl_t perplexity(const wstring & text) noexcept {
			// Выполняем расчёт перплексии
			return (almV2 ? alm2->perplexity(text) : alm1->perplexity(text));
		}
		/**
		 * perplexity Метод расчёта перплексии
		 * @param  seq список последовательностей
		 * @return     результат расчёта
		 */
		const alm_t::ppl_t perplexity(const vector <size_t> & seq) noexcept {
			// Выполняем расчёт перплексии
			return (almV2 ? alm2->perplexity(seq) : alm1->perplexity(seq));
		}
		/**
		 * pplConcatenate Метод объединения перплексий
		 * @param ppl1 первая перплексия
		 * @param ppl2 вторая перплексия
		 * @return     объединённая перплексия
		 */
		const alm_t::ppl_t pplConcatenate(const alm_t::ppl_t & ppl1, const alm_t::ppl_t & ppl2) noexcept {
			// Выполняем расчёт перплексии
			return (almV2 ? alm2->pplConcatenate(ppl1, ppl2) : alm1->pplConcatenate(ppl1, ppl2));
		}
		/**
		 * countTrigrams Метод проверки количества найденных в тексте триграмм
		 * @param text текст для расчёта
		 * @return     количество найденных триграмм
		 */
		const size_t countTrigrams(const wstring & text) noexcept {
			// Выводим результат
			return (almV2 ? alm2->trigrams(alphabet.convert(text)) : alm1->trigrams(alphabet.convert(text)));
		}
		/**
		 * countTrigrams Метод проверки количества найденных триграмм
		 * @param seq список последовательностей
		 * @return    количество найденных триграмм
		 */
		const size_t countTrigrams(const vector <size_t> & seq) noexcept {
			// Выводим результат
			return (almV2 ? alm2->trigrams(seq) : alm1->trigrams(seq));
		}
		/**
		 * countGrams Метод проверки количества найденных в тексте n-грамм
		 * @param text текст для расчёта
		 * @return     количество найденных n-грамм
		 */
		const size_t countGrams(const wstring & text) noexcept {
			// Выводим результат
			return (almV2 ? alm2->grams(alphabet.convert(text)) : alm1->grams(alphabet.convert(text)));
		}
		/**
		 * countGrams Метод проверки количества найденных n-грамм
		 * @param seq список последовательностей
		 * @return    количество найденных n-грамм
		 */
		const size_t countGrams(const vector <size_t> & seq) noexcept {
			// Выводим результат
			return (almV2 ? alm2->grams(seq) : alm1->grams(seq));
		}
		/**
		 * countBigrams Метод проверки количества найденных в тексте биграмм
		 * @param text текст для расчёта
		 * @return     количество найденных биграмм
		 */
		const size_t countBigrams(const wstring & text) noexcept {
			// Выводим результат
			return (almV2 ? alm2->bigrams(alphabet.convert(text)) : alm1->bigrams(alphabet.convert(text)));
		}
		/**
		 * countBigrams Метод проверки количества найденных биграмм
		 * @param seq список последовательностей
		 * @return    количество найденных биграмм
		 */
		const size_t countBigrams(const vector <size_t> & seq) noexcept {
			// Выводим результат
			return (almV2 ? alm2->bigrams(seq) : alm1->bigrams(seq));
		}
		/**
		 * arabic2Roman Метод перевода арабских чисел в римские
		 * @param  number арабское число от 1 до 4999
		 * @return        римское число
		 */
		const wstring arabic2Roman(const size_t number) noexcept {
			// Выполняем конвертацию чисел
			return alphabet.arabic2Roman(number);
		}
		/**
		 * arabic2Roman Метод перевода арабских чисел в римские
		 * @param  word арабское число от 1 до 4999
		 * @return      римское число
		 */
		const wstring arabic2Roman(const wstring & word) noexcept {
			// Выполняем конвертацию чисел
			return alphabet.arabic2Roman(word);
		}
		/**
		 * roman2Arabic Метод перевода римских цифр в арабские
		 * @param  word римское число
		 * @return      арабское число
		 */
		const size_t roman2Arabic(const wstring & word) noexcept {
			// Выводим конвертацию чисел
			return alphabet.roman2Arabic(alphabet.toLower(word));
		}
		/**
		 * countAlphabet Метод получения количества букв в словаре
		 * @return количество букв в словаре
		 */
		const size_t countAlphabet() noexcept {
			// Выводим количество букв в словаре
			return alphabet.count();
		}
		/**
		 * isToken Метод проверки идентификатора на токен
		 * @param idw идентификатор слова для проверки
		 * @return    результат проверки
		 */
		const bool isToken(const size_t idw) noexcept {
			// Выполняем проверку на токен
			return tokenizer.isToken(idw);
		}
		/**
		 * isIdWord Метод проверки на соответствие идентификатора слову
		 * @param idw идентификатор слова для проверки
		 * @return    результат проверки идентификатора
		 */
		const bool isIdWord(const size_t idw) noexcept {
			// Выполняем проверку на соответствие токена разрешённому слову
			return tokenizer.isIdWord(idw);
		}
		/**
		 * isAbbr Метод проверки слова на соответствие аббревиатуры
		 * @param idw идентификатор слова для проверки
		 * @return    результат проверки
		 */
		const bool isAbbr(const size_t idw) noexcept {
			// Выводим результат проверки на аббревиатуру
			return tokenizer.isAbbr(idw);
		}
		/**
		 * isAbbr Метод проверки слова на соответствие аббревиатуры
		 * @param  word слово для проверки
		 * @return      результат проверки
		 */
		const bool isAbbr(const wstring & word) noexcept {
			// Выводим результат проверки на аббревиатуру
			return tokenizer.isAbbr(word);
		}
		/**
		 * isSuffix Метод проверки слова на суффикс цифровой аббревиатуры
		 * @param  word слово для проверки
		 * @return      результат проверки
		 */
		const bool isSuffix(const wstring & word) noexcept {
			// Выводим результат проверки на суффикс цифровой аббревиатуры
			return tokenizer.isSuffix(word);
		}
		/**
		 * isAllowApostrophe Метод проверки разрешения апострофа
		 * @return результат проверки
		 */
		const bool isAllowApostrophe() noexcept {
			// Выводрим результат проверки
			return alphabet.isAllowApostrophe();
		}
		/**
		 * checkSequence Метод проверки существования последовательности
		 * @param text     текст для проверки существования
		 * @param accurate режим точной проверки
		 * @return         результат проверки
		 */
		const pair <bool, size_t> checkSequence(const wstring & text, const bool accurate = false) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->check(text, accurate) : alm1->check(text, accurate));
		}
		/**
		 * checkSequence Метод проверки существования последовательности, с указанным шагом
		 * @param text текст для проверки существования
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const bool checkSequence(const wstring & text, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->check(text, step) : alm1->check(text, step));
		}
		/**
		 * checkSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const bool checkSequence(const vector <wstring> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->check(seq, step) : alm1->check(seq, step));
		}
		/**
		 * checkSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const bool checkSequence(const vector <size_t> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->check(seq, step) : alm1->check(seq, step));
		}
		/**
		 * existSequence Метод проверки существования последовательности, с указанным шагом
		 * @param text текст для проверки существования
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const pair <bool, size_t> existSequence(const wstring & text, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->exist(text, step) : alm1->exist(text, step));
		}
		/**
		 * existSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const pair <bool, size_t> existSequence(const vector <wstring> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->exist(seq, step) : alm1->exist(seq, step));
		}
		/**
		 * existSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const pair <bool, size_t> existSequence(const vector <size_t> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->exist(seq, step) : alm1->exist(seq, step));
		}
		/**
		 * findByFiles Метод поиска n-грамм в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void findByFiles(const wstring & path, const wstring & filename, const wstring & ext = L"txt") noexcept {
			// Выполняем поиск n-грамм в текстовом файле
			if(almV2)
				// Выполняем поиск n-грамм в текстовом файле для ALMv2
				alm2->findByFiles(alphabet.convert(path), alphabet.convert(filename), nullptr, alphabet.convert(ext));
			// Выполняем поиск n-грамм в текстовом файле для ALMv1
			else alm1->findByFiles(alphabet.convert(path), alphabet.convert(filename), nullptr, alphabet.convert(ext));
		}
		/**
		 * pplByFiles Метод чтения расчёта перплексии по файлу или группе файлов
		 * @param path адрес каталога или файла для расчёта перплексии
		 * @param ext  расширение файлов в каталоге (если адрес передан каталога)
		 * @return     результат расчёта
		 */
		const alm_t::ppl_t pplByFiles(const wstring & path, const wstring & ext = L"txt") noexcept {
			// Выполняем расчёт перплексии
			return (almV2 ? alm2->pplByFiles(alphabet.convert(path), nullptr, alphabet.convert(ext)) : alm1->pplByFiles(alphabet.convert(path), nullptr, alphabet.convert(ext)));
		}
		/**
		 * checkSequence Метод проверки существования последовательности
		 * @param seq      список слов последовательности
		 * @param accurate режим точной проверки
		 * @return         результат проверки
		 */
		const pair <bool, size_t> checkSequence(const vector <size_t> & seq, const bool accurate = false) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->check(seq, accurate) : alm1->check(seq, accurate));
		}
		/**
		 * checkSequence Метод проверки существования последовательности
		 * @param seq      список слов последовательности
		 * @param accurate режим точной проверки
		 * @return         результат проверки
		 */
		const pair <bool, size_t> checkSequence(const vector <wstring> & seq, const bool accurate = false) noexcept {
			// Выполняем проверку существования последовательности
			return (almV2 ? alm2->check(seq, accurate) : alm1->check(seq, accurate));
		}
		/**
		 * sentences Метод генерации предложений
		 * @param callback функция обратного вызова
		 */
		void sentences(function <const bool (const wstring &)> callback) noexcept {
			// Выполняем генерацию предложений
			(almV2 ? alm2->sentences(callback) : alm1->sentences(callback));
		}
		/**
		 * sentencesToFile Метод сборки указанного количества предложений и записи в файл
		 * @param counts   количество предложений для сборки
		 * @param filename адрес файла для записи результата
		 */
		void sentencesToFile(const size_t counts, const wstring & filename) noexcept {
			// Выполняем сборку указанного количества предложений
			(almV2 ? alm2->sentencesToFile(counts, alphabet.convert(filename)) : alm1->sentencesToFile(counts, alphabet.convert(filename)));
		}
		/**
		 * findNgram Метод поиска n-грамм в тексте
		 * @param text     текст в котором необходимо найти n-граммы
		 * @param callback функция обратного вызова
		 */
		void findNgram(const wstring & text, function <void (const wstring &)> callback) noexcept {
			// Выполняем поиск n-грамм в тексте
			(almV2 ? alm2->find(text, callback) : alm1->find(text, callback));
		}
		/**
		 * fixUppersByFiles Метод исправления регистров текста в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void fixUppersByFiles(const wstring & path, const wstring & filename, const wstring & ext = L"txt") noexcept {
			// Выполняем исправление регистров текста
			if(almV2)
				// Выполняем исправление регистров текста для ALMv2
				alm2->fixUppersByFiles(alphabet.convert(path), alphabet.convert(filename), nullptr, alphabet.convert(ext));
			// Выполняем исправление регистров текста для ALMv1
			else alm1->fixUppersByFiles(alphabet.convert(path), alphabet.convert(filename), nullptr, alphabet.convert(ext));
		}
		/**
		 * countsByFiles Метод подсчёта количества n-грамм в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param ngrams   размер n-граммы для подсчёта
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void countsByFiles(const wstring & path, const wstring & filename, const u_short ngrams = 0, const wstring & ext = L"txt") noexcept {
			// Выполняем подсчёт количества n-грамм
			if(almV2)
				// Выполняем подсчёт количества n-грамм для ALMv2
				alm2->countsByFiles(alphabet.convert(path), alphabet.convert(filename), ngrams, nullptr, alphabet.convert(ext));
			// Выполняем подсчёт количества n-грамм для ALMv1
			else alm1->countsByFiles(alphabet.convert(path), alphabet.convert(filename), ngrams, nullptr, alphabet.convert(ext));
		}
		/**
		 * checkByFiles Метод проверки существования последовательности в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param accurate режим точной проверки
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void checkByFiles(const wstring & path, const wstring & filename, const bool accurate = false, const wstring & ext = L"txt") noexcept {
			// Выполняем проверку существования последовательности
			if(almV2)
				// Выполняем проверку существования последовательности для ALMv2
				alm2->checkByFiles(alphabet.convert(path), alphabet.convert(filename), accurate, nullptr, alphabet.convert(ext));
			// Выполняем проверку существования последовательности для ALMv1
			else alm1->checkByFiles(alphabet.convert(path), alphabet.convert(filename), accurate, nullptr, alphabet.convert(ext));
		}
		/**
		 * setTokenizerFn Метод установки функции внешнего токенизатора
		 * @param fn функция внешнего токенизатора
		 */
		void setTokenizerFn(function <void (const wstring &, function <const bool (const wstring &, const vector <string> &, const bool, const bool)>)> fn) noexcept {
			// Устанавливаем функцию внешнего токенизатора
			tokenizer.setExternal(fn);
		}
	};
};
// asc Регистрируем имя модуля спеллчекера
PYBIND11_MODULE(asc, m) {
	/**
	 * Устанавливаем флаги библиотеки
	 */
	// Список флагов для удаления в тексе символов
	py::enum_ <anyks::wdel_t> (m, "wdel_t")
	.value("punct", anyks::wdel_t::punct)
	.value("broken", anyks::wdel_t::broken)
	.value("hyphen", anyks::wdel_t::hyphen)
	.export_values();
	// Список флагов для проверки текста
	py::enum_ <anyks::check_t> (m, "check_t")
	.value("home2", anyks::check_t::home2)
	.value("latian", anyks::check_t::latian)
	.value("hyphen", anyks::check_t::hyphen)
	.value("letter", anyks::check_t::letter)
	.value("similars", anyks::check_t::similars)
	.export_values();
	// Список флагов для очистки текста
	py::enum_ <anyks::clear_t> (m, "clear_t")
	.value("all", anyks::clear_t::all)
	.value("utokens", anyks::clear_t::utokens)
	.value("badwords", anyks::clear_t::badwords)
	.value("goodwords", anyks::clear_t::goodwords)
	.export_values();
	// Список флагов типов сглаживания
	py::enum_ <anyks::smoothing_t> (m, "smoothing_t")
	.value("wittenBell", anyks::smoothing_t::wittenBell)
	.value("addSmooth", anyks::smoothing_t::addSmooth)
	.value("kneserNey", anyks::smoothing_t::kneserNey)
	.value("goodTuring", anyks::smoothing_t::goodTuring)
	.value("modKneserNey", anyks::smoothing_t::modKneserNey)
	.value("constDiscount", anyks::smoothing_t::constDiscount)
	.value("naturalDiscount", anyks::smoothing_t::naturalDiscount)
	.export_values();
	// Список флагов для матчинга текста
	py::enum_ <anyks::match_t> (m, "match_t")
	.value("url", anyks::match_t::url)
	.value("abbr", anyks::match_t::abbr)
	.value("math", anyks::match_t::math)
	.value("greek", anyks::match_t::greek)
	.value("route", anyks::match_t::route)
	.value("upper", anyks::match_t::upper)
	.value("punct", anyks::match_t::punct)
	.value("space", anyks::match_t::space)
	.value("letter", anyks::match_t::letter)
	.value("pcards", anyks::match_t::pcards)
	.value("latian", anyks::match_t::latian)
	.value("number", anyks::match_t::number)
	.value("anumber", anyks::match_t::anumber)
	.value("allowed", anyks::match_t::allowed)
	.value("decimal", anyks::match_t::decimal)
	.value("special", anyks::match_t::special)
	.value("currency", anyks::match_t::currency)
	.value("isolation", anyks::match_t::isolation)
	.export_values();
	// Список флагов основных опций библиотеки
	py::enum_ <anyks::options_t> (m, "options_t")
	.value("debug", anyks::options_t::debug)
	.value("bloom", anyks::options_t::bloom)
	.value("stress", anyks::options_t::stress)
	.value("uppers", anyks::options_t::uppers)
	.value("collect", anyks::options_t::collect)
	.value("allGrams", anyks::options_t::allGrams)
	.value("allowUnk", anyks::options_t::allowUnk)
	.value("resetUnk", anyks::options_t::resetUnk)
	.value("stemming", anyks::options_t::stemming)
	.value("onlyGood", anyks::options_t::onlyGood)
	.value("mixDicts", anyks::options_t::mixdicts)
	.value("onlyTypos", anyks::options_t::onlytypos)
	.value("lowerCase", anyks::options_t::lowerCase)
	.value("tokenWords", anyks::options_t::tokenWords)
	.value("confidence", anyks::options_t::confidence)
	.value("interpolate", anyks::options_t::interpolate)
	.value("ascSplit", anyks::options_t::ascsplit)
	.value("ascAlter", anyks::options_t::ascalter)
	.value("ascESplit", anyks::options_t::ascesplit)
	.value("ascRSplit", anyks::options_t::ascrsplit)
	.value("ascUppers", anyks::options_t::ascuppers)
	.value("ascHyphen", anyks::options_t::aschyphen)
	.value("ascSkipUpp", anyks::options_t::ascskipupp)
	.value("ascSkipLat", anyks::options_t::ascskiplat)
	.value("ascSkipHyp", anyks::options_t::ascskiphyp)
	.value("ascWordRep", anyks::options_t::ascwordrep)
	.export_values();
	// Структура параметров расчёта перплексии
	py::class_ <anyks::alm_t::ppl_t> (m, "ppl_t")
	.def(py::init())
	.def_readwrite("oovs", &anyks::alm_t::ppl_t::oovs)
	.def_readwrite("words", &anyks::alm_t::ppl_t::words)
	.def_readwrite("sentences", &anyks::alm_t::ppl_t::sentences)
	.def_readwrite("zeroprobs", &anyks::alm_t::ppl_t::zeroprobs)
	.def_readwrite("logprob", &anyks::alm_t::ppl_t::logprob)
	.def_readwrite("ppl", &anyks::alm_t::ppl_t::ppl)
	.def_readwrite("ppl1", &anyks::alm_t::ppl_t::ppl1);
	/**
	 * Устанавливаем методы объекта
	 */
	{
		// idt Метод извлечения идентификатора токена
		m.def("idt", &anyks::Methods::idt, "Token ID retrieval method", py::call_guard <py::gil_scoped_release>())
		// ids Метод извлечения идентификатора последовательности
		.def("ids", &anyks::Methods::ids, "Sequence ID retrieval method", py::call_guard <py::gil_scoped_release>())
		// setZone Метод установки пользовательской зоны
		.def("setZone", &anyks::Methods::setZone, "User zone set method", py::call_guard <py::gil_scoped_release>())
		// setCode Метод установки кода языка
		.def("setCode", &anyks::Methods::setCode, "Method for set code language", py::call_guard <py::gil_scoped_release>())
		// getName Метод извлечения названия библиотеки
		.def("getName", &anyks::Methods::getName, "Library name retrieval method", py::call_guard <py::gil_scoped_release>())
		// setPilots Метод установки пилотных слов
		.def("setPilots", &anyks::Methods::setPilots, "Method for set pilot words", py::call_guard <py::gil_scoped_release>())
		// setName Метод установки названия словаря
		.def("setName", &anyks::Methods::setName, "Method for set dictionary name", py::call_guard <py::gil_scoped_release>())
		// erratum Метод поиска в тексте опечаток
		.def("erratum", &anyks::Methods::erratum, "Method for search typos in text", py::call_guard <py::gil_scoped_release>())
		// isToken Метод проверки идентификатора на токен
		.def("isToken", &anyks::Methods::isToken, "Checking a word against a token", py::call_guard <py::gil_scoped_release>())
		// sentences Метод генерации предложений
		.def("sentences", &anyks::Methods::sentences, "Sentences generation method", py::call_guard <py::gil_scoped_release>())
		// getEmail Метод извлечения электронной почты автора
		.def("getEmail", &anyks::Methods::getEmail, "Author email retrieval method", py::call_guard <py::gil_scoped_release>())
		// getPhone Метод извлечения телефона автора
		.def("getPhone", &anyks::Methods::getPhone, "Author phone retrieval method", py::call_guard <py::gil_scoped_release>())
		// setAlphabet Метод установки алфавита
		.def("setAlphabet", &anyks::Methods::setAlphabet, "Method for set Alphabet", py::call_guard <py::gil_scoped_release>())
		// find Метод поиска n-грамм в тексте
		.def("findNgram", &anyks::Methods::findNgram, "N-gram search method in text", py::call_guard <py::gil_scoped_release>())
		// getAuthor Метод извлечения имени автора
		.def("getAuthor", &anyks::Methods::getAuthor, "Author name retrieval method", py::call_guard <py::gil_scoped_release>())
		// isIdWord Метод проверки на соответствие идентификатора слову
		.def("isIdWord", &anyks::Methods::isIdWord, "Checking a token against a word", py::call_guard <py::gil_scoped_release>())
		// setOption Метод установки опций модуля языковой модели
		.def("setOption", &anyks::Methods::setOption, "Method for set module options", py::call_guard <py::gil_scoped_release>())
		// setUnknown Метод установки неизвестного слова
		.def("setUnknown", &anyks::Methods::setUnknown, "Method for set unknown word", py::call_guard <py::gil_scoped_release>())
		// setEmbedding Метод установки эмбеддинга
		.def("setEmbedding", &anyks::Methods::setEmbedding, "Method for set embedding", py::call_guard <py::gil_scoped_release>())
		// analyze Метод выполнения анализа текста
		.def("analyze", &anyks::Methods::analyze, "Method for performing text analysis", py::call_guard <py::gil_scoped_release>())
		// size Метод получения размера n-грамы
		.def("size", &anyks::Methods::size, "Method of obtaining the size of the N-gram", py::call_guard <py::gil_scoped_release>())
		// jsonToText Метод преобразования текста в формате json в текст
		.def("jsonToText", &anyks::Methods::jsonToText, "Method to convert JSON to text", py::call_guard <py::gil_scoped_release>())
		// textToJson Метод преобразования текста в json
		.def("textToJson", &anyks::Methods::textToJson, "Method to convert text to JSON", py::call_guard <py::gil_scoped_release>())
		// restore Метод восстановления текста из контекста
		.def("restore", &anyks::Methods::restore, "Method for restore text from context", py::call_guard <py::gil_scoped_release>())
		// unsetOption Метод отключения опции модуля
		.def("unsetOption", &anyks::Methods::unsetOption, "Disable module option method", py::call_guard <py::gil_scoped_release>())
		// getBadwords Метод извлечения чёрного списка
		.def("getBadwords", &anyks::Methods::getBadwords, "Method get words in blacklist", py::call_guard <py::gil_scoped_release>())
		// setUserToken Метод добавления токена пользователя
		.def("setUserToken", &anyks::Methods::setUserToken, "Method for adding user token", py::call_guard <py::gil_scoped_release>())
		// getGoodwords Метод извлечения белого списка
		.def("getGoodwords", &anyks::Methods::getGoodwords, "Method get words in whitelist", py::call_guard <py::gil_scoped_release>())
		// setAuthor Метод установки автора словаря
		.def("setAuthor", &anyks::Methods::setAuthor, "Method for set the dictionary author", py::call_guard <py::gil_scoped_release>())
		// getUnknown Метод извлечения неизвестного слова
		.def("getUnknown", &anyks::Methods::getUnknown, "Method for extraction unknown word", py::call_guard <py::gil_scoped_release>())
		// setAlmV2 Метод установки типа языковой модели
		.def("setAlmV2", &anyks::Methods::setAlmV2, "Method for set the language model type", py::call_guard <py::gil_scoped_release>())
		// split Метод выполнения разбивку слипшихся слов
		.def("split", &anyks::Methods::split, "Method for performing a split of clumped words", py::call_guard <py::gil_scoped_release>())
		// addLemma Метод добавления леммы в словарь
		.def("addLemma", &anyks::Methods::addLemma, "Method for add a Lemma to the dictionary", py::call_guard <py::gil_scoped_release>())
		// pplConcatenate Метод объединения перплексий
		.def("pplConcatenate", &anyks::Methods::pplConcatenate, "Method of combining perplexia", py::call_guard <py::gil_scoped_release>())
		// setLogfile Метод установки файла для вывода логов
		.def("setLogfile", &anyks::Methods::setLogfile, "Method of set the file for log output", py::call_guard <py::gil_scoped_release>())
		// setOOvFile Метод установки файла для сохранения OOV слов
		.def("setOOvFile", &anyks::Methods::setOOvFile, "Method set file for saving OOVs words", py::call_guard <py::gil_scoped_release>())
		// getUserTokens Метод извлечения списка пользовательских токенов
		.def("getUserTokens", &anyks::Methods::getUserTokens, "User token list retrieval method", py::call_guard <py::gil_scoped_release>())
		// setAlmV2 Метод установки типа языковой модели
		.def("unsetAlmV2", &anyks::Methods::unsetAlmV2, "Method for unset the language model type", py::call_guard <py::gil_scoped_release>())
		// token Метод определения типа токена слова
		.def("token", &anyks::Methods::token, "Method for determining the type of the token words", py::call_guard <py::gil_scoped_release>())
		// allowStress Метод разрешения, использовать ударение в словах
		.def("allowStress", &anyks::Methods::allowStress, "Method for allow using stress in words", py::call_guard <py::gil_scoped_release>())
		// tokenization Метод разбивки текста на токены
		.def("tokenization", &anyks::Methods::tokenization, "Method for breaking text into tokens", py::call_guard <py::gil_scoped_release>())
		// fixUppers Метод исправления регистров в тексте
		.def("fixUppers", &anyks::Methods::fixUppers, "Method for correcting registers in the text", py::call_guard <py::gil_scoped_release>())
		// checkHypLat Метод поиска дефиса и латинского символа
		.def("checkHypLat", &anyks::Methods::checkHypLat, "Hyphen and latin character search method", py::call_guard <py::gil_scoped_release>())
		// getContact Метод извлечения контактных данных автора
		.def("getContact", &anyks::Methods::getContact, "Author contact information retrieval method", py::call_guard <py::gil_scoped_release>())
		// getAbbrs Метод извлечения списка аббревиатур
		.def("getAbbrs", &anyks::Methods::getAbbrs, "Method for extracting the list of abbreviations", py::call_guard <py::gil_scoped_release>())
		// getSite Метод извлечения адреса сайта автора
		.def("getSite", &anyks::Methods::getSite, "Method for extracting the author’s website address", py::call_guard <py::gil_scoped_release>())
		// getAlphabet Метод получения алфавита языка
		.def("getAlphabet", &anyks::Methods::getAlphabet, "Method for obtaining the language alphabet", py::call_guard <py::gil_scoped_release>())
		// setCopyright Метод установки авторских прав на словарь
		.def("setCopyright", &anyks::Methods::setCopyright, "Method for set copyright on a dictionary", py::call_guard <py::gil_scoped_release>())
		// generateEmbedding Метод генерации эмбеддинга
		.def("generateEmbedding", &anyks::Methods::generateEmbedding, "Method for generation embedding", py::call_guard <py::gil_scoped_release>())
		// urls Метод извлечения координат url адресов в строке
		.def("urls", &anyks::Methods::urls, "Method for extracting URL address coordinates in a string", py::call_guard <py::gil_scoped_release>())
		// setSizeEmbedding Метод установки размера эмбеддинга
		.def("setSizeEmbedding", &anyks::Methods::setSizeEmbedding, "Method for set the embedding size", py::call_guard <py::gil_scoped_release>())
		// setLictext Метод установки лицензионной информации словаря
		.def("setLictext", &anyks::Methods::setLictext, "Method for set license information dictionary", py::call_guard <py::gil_scoped_release>())
		// infoIndex Метод вывода информации о словаре
		.def("infoIndex", &anyks::Methods::infoIndex, "Method for print information about the dictionary", py::call_guard <py::gil_scoped_release>())
		// getVersion Метод получения версии языковой модели
		.def("getVersion", &anyks::Methods::getVersion, "Method for obtaining the language model version", py::call_guard <py::gil_scoped_release>())
		// isAllowApostrophe Метод проверки разрешения апострофа
		.def("isAllowApostrophe", &anyks::Methods::isAllowApostrophe, "Apostrophe permission check method", py::call_guard <py::gil_scoped_release>())
		// disallowStress Метод запрещения использовать ударение в словах
		.def("disallowStress", &anyks::Methods::disallowStress, "Method for disallow using stress in words", py::call_guard <py::gil_scoped_release>())
		// getUserTokenId Метод получения идентификатора пользовательского токена
		.def("getUserTokenId", &anyks::Methods::getUserTokenId, "Method for obtaining user token identifier", py::call_guard <py::gil_scoped_release>())
		// setLictype Метод установки типа лицензионной информации словаря
		.def("setLictype", &anyks::Methods::setLictype, "Method for set dictionary license information type", py::call_guard <py::gil_scoped_release>())
		// roman2Arabic Метод перевода римских цифр в арабские
		.def("roman2Arabic", &anyks::Methods::roman2Arabic, "Method for translating Roman numerals to Arabic", py::call_guard <py::gil_scoped_release>())
		// setStemmingMethod Метод установки функции получения леммы
		.def("setStemmingMethod", &anyks::Methods::setStemmingMethod, "Method for set the Lemma get function", py::call_guard <py::gil_scoped_acquire>())
		// rest Метод исправления и детектирования слов со смешанными алфавитами
		.def("rest", &anyks::Methods::rest, "Method for correction and detection of words with mixed alphabets", py::call_guard <py::gil_scoped_release>())
		// setTokensDisable Метод установки списка запрещённых токенов
		.def("setTokensDisable", &anyks::Methods::setTokensDisable, "Method for set the list of forbidden tokens", py::call_guard <py::gil_scoped_release>())
		// setContacts Метод установки контактных данных автора словаря
		.def("setContacts", &anyks::Methods::setContacts, "Method for set contact details of the dictionary author", py::call_guard <py::gil_scoped_release>())
		// setTokenDisable Метод установки списка не идентифицируемых токенов
		.def("setTokenDisable", &anyks::Methods::setTokenDisable, "Method for set the list of unidentifiable tokens", py::call_guard <py::gil_scoped_release>())
		// setVariantsMethod Метод установки функции подбора вариантов
		.def("setVariantsMethod", &anyks::Methods::setVariantsMethod, "Method for set the option selection function", py::call_guard <py::gil_scoped_release>())
		// setAllTokenDisable Метод установки всех токенов как не идентифицируемых
		.def("setAllTokenDisable", &anyks::Methods::setAllTokenDisable, "Method for set all tokens as unidentifiable", py::call_guard <py::gil_scoped_release>())
		// setTokensUnknown Метод установки списка токенов приводимых к <unk>
		.def("setTokensUnknown", &anyks::Methods::setTokensUnknown, "Method for set the list of tokens cast to <unk>", py::call_guard <py::gil_scoped_release>())
		// setTokenizerFn Метод установки функции внешнего токенизатора
		.def("setTokenizerFn", &anyks::Methods::setTokenizerFn, "Method for set the function of an external tokenizer", py::call_guard <py::gil_scoped_release>())
		// getTokensDisable Метод извлечения списка запрещённых токенов
		.def("getTokensDisable", &anyks::Methods::getTokensDisable, "Method for retrieving the list of forbidden tokens", py::call_guard <py::gil_scoped_release>())
		// countLetter Метод подсчета количества указанной буквы в слове
		.def("countLetter", &anyks::Methods::countLetter, "Method for counting the amount of a specific letter in a word", py::call_guard <py::gil_scoped_release>())
		// setAllTokenUnknown Метод установки всех токенов идентифицируемых как <unk>
		.def("setAllTokenUnknown", &anyks::Methods::setAllTokenUnknown, "The method of set all tokens identified as <unk>", py::call_guard <py::gil_scoped_release>())
		// countAlphabet Метод получения количества букв в словаре
		.def("countAlphabet", &anyks::Methods::countAlphabet, "Method of obtaining the number of letters in the dictionary", py::call_guard <py::gil_scoped_release>())
		// getUserTokenWord Метод получения пользовательского токена по его идентификатору
		.def("getUserTokenWord", &anyks::Methods::getUserTokenWord, "Method for obtaining a custom token by its identifier", py::call_guard <py::gil_scoped_release>())
		// setUserTokenMethod Метод добавления функции обработки пользовательского токена
		.def("setUserTokenMethod", &anyks::Methods::setUserTokenMethod, "Method for set a custom token processing function", py::call_guard <py::gil_scoped_release>())
		// splitByHyphens Метод выполнения разбивку слипшихся слов по дефисам
		.def("splitByHyphens", &anyks::Methods::splitByHyphens, "Method for performing a split of clumped words by hyphens", py::call_guard <py::gil_scoped_release>())
		// distanceLevenshtein Определение дистанции Левенштейна в фразах
		.def("distanceLevenshtein", &anyks::Methods::distanceLevenshtein, "Determination of Levenshtein distance in phrases", py::call_guard <py::gil_scoped_release>())
		// setSubstitutes Метод установки букв для исправления слов из смешанных алфавитов
		.def("setSubstitutes", &anyks::Methods::setSubstitutes, "Method for set letters to correct words from mixed alphabets", py::call_guard <py::gil_scoped_release>())
		// getTokensUnknown Метод извлечения списка токенов приводимых к <unk>
		.def("getTokensUnknown", &anyks::Methods::getTokensUnknown, "Method for extracting a list of tokens reducible to <unk>", py::call_guard <py::gil_scoped_release>())
		// getSuffixes Метод извлечения списка суффиксов цифровых аббревиатур
		.def("getSuffixes", &anyks::Methods::getSuffixes, "Method for extracting the list of suffixes of digital abbreviations", py::call_guard <py::gil_scoped_release>())
		// getSubstitutes Метод извлечения букв для исправления слов из смешанных алфавитов
		.def("getSubstitutes", &anyks::Methods::getSubstitutes, "Method of extracting letters to correct words from mixed alphabets", py::call_guard <py::gil_scoped_release>())
		// damerauLevenshtein Определение дистанции Дамерау-Левенштейна в фразах
		.def("damerauLevenshtein", &anyks::Methods::damerauLevenshtein, "Determination of the Damerau-Levenshtein distance in phrases", py::call_guard <py::gil_scoped_release>())
		// setTokenUnknown Метод установки списка токенов которых нужно идентифицировать как <unk>
		.def("setTokenUnknown", &anyks::Methods::setTokenUnknown, "Method of set the list of tokens that need to be identified as <unk>", py::call_guard <py::gil_scoped_release>())
		// setWordPreprocessingMethod Метод установки функции препроцессинга слова
		.def("setWordPreprocessingMethod", &anyks::Methods::setWordPreprocessingMethod, "Method for set the word preprocessing function", py::call_guard <py::gil_scoped_release>())
		// mulctLevenshtein Определение количества штрафов на основе Дамерау-Левенштейна
		.def("mulctLevenshtein", &anyks::Methods::mulctLevenshtein, "Determination of the number of penalties based on Damerau-Levenshtein", py::call_guard <py::gil_scoped_release>())
		// setUWords Метод добавления списка идентификаторов слов, которые всегда начинаются с заглавной буквы
		.def("setUWords", &anyks::Methods::setUWords, "Method for add a list of identifiers for words that always start with a capital letter", py::call_guard <py::gil_scoped_release>())
		// switchAllowApostrophe Метод разрешения или запрещения апострофа как части слова
		.def("switchAllowApostrophe", &anyks::Methods::switchAllowApostrophe, "Method for permitting or denying an apostrophe as part of a word", py::call_guard <py::gil_scoped_release>());
	}{
		// addAbbr Метод добавления аббревиатуры в виде идентификатора
		m.def("addAbbr", overload_cast_ <const size_t> ()(&anyks::Methods::addAbbr), "Method add abbreviation", py::call_guard <py::gil_scoped_release>())
		// addAbbr Метод добавления аббревиатуры в виде слова
		.def("addAbbr", overload_cast_ <const wstring &> ()(&anyks::Methods::addAbbr), "Method add abbreviation", py::call_guard <py::gil_scoped_release>())
		// addBadword Метод добавления похого слова в список
		.def("addBadword", overload_cast_ <const wstring &> ()(&anyks::Methods::addBadword), "Method add bad word", py::call_guard <py::gil_scoped_release>())
		// addGoodIdw Метод добавления идентификатора похого слова в список
		.def("addBadword", overload_cast_ <const size_t> ()(&anyks::Methods::addBadword), "Method add bad idw word", py::call_guard <py::gil_scoped_release>())
		// perplexity Метод расчёта перплексии текста
		.def("perplexity", overload_cast_ <const wstring &> ()(&anyks::Methods::perplexity), "Perplexity calculation", py::call_guard <py::gil_scoped_release>())
		// addGoodword Метод добавления идентификатора хорошего слова в список
		.def("addGoodword", overload_cast_ <const wstring &> ()(&anyks::Methods::addGoodword), "Method add good word", py::call_guard <py::gil_scoped_release>())
		// addGoodword Метод добавления хорошего слова в список
		.def("addGoodword", overload_cast_ <const size_t> ()(&anyks::Methods::addGoodword), "Method add good idw word", py::call_guard <py::gil_scoped_release>())
		// setAbbrs Метод установки списка идентификаторов аббревиатур
		.def("setAbbrs", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setAbbrs), "Method set abbreviations", py::call_guard <py::gil_scoped_release>())
		// isAbbr Метод проверки слова на соответствие аббревиатуры
		.def("isAbbr", overload_cast_ <const size_t> ()(&anyks::Methods::isAbbr), "Checking a word against a abbreviation", py::call_guard <py::gil_scoped_release>())
		// countBigrams Метод проверки количества найденных биграмм
		.def("countBigrams", overload_cast_ <const wstring &> ()(&anyks::Methods::countBigrams), "Method get count bigrams", py::call_guard <py::gil_scoped_release>())
		// perplexity Метод расчёта перплексии текста
		.def("perplexity", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::perplexity), "Perplexity calculation", py::call_guard <py::gil_scoped_release>())
		// isAbbr Метод проверки слова на соответствие аббревиатуры
		.def("isAbbr", overload_cast_ <const wstring &> ()(&anyks::Methods::isAbbr), "Checking a word against a abbreviation", py::call_guard <py::gil_scoped_release>())
		// countTrigrams Метод проверки количества найденных триграмм
		.def("countTrigrams", overload_cast_ <const wstring &> ()(&anyks::Methods::countTrigrams), "Method get count trigrams", py::call_guard <py::gil_scoped_release>())
		// Метод добавления идентификатора суффикса цифровой аббреувиатуры
		.def("addSuffix", overload_cast_ <const size_t> ()(&anyks::Methods::addSuffix), "Method add number suffix abbreviation", py::call_guard <py::gil_scoped_release>())
		// countGrams Метод проверки количества найденных n-грамм
		.def("countGrams", overload_cast_ <const wstring &> ()(&anyks::Methods::countGrams), "Method get count N-gram by lm size", py::call_guard <py::gil_scoped_release>())
		// countBigrams Метод проверки количества найденных биграмм
		.def("countBigrams", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::countBigrams), "Method get count bigrams", py::call_guard <py::gil_scoped_release>())
		// arabic2Roman Метод перевода арабских чисел в римские
		.def("arabic2Roman", overload_cast_ <const size_t> ()(&anyks::Methods::arabic2Roman), "Convert arabic number to roman number", py::call_guard <py::gil_scoped_release>())
		// countTrigrams Метод проверки количества найденных триграмм
		.def("countTrigrams", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::countTrigrams), "Method get count trigrams", py::call_guard <py::gil_scoped_release>())
		// setBadwords Метод установки списка идентификаторов плохих слов в список
		.def("setBadwords", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setBadwords), "Method set idw words to blacklist", py::call_guard <py::gil_scoped_release>())
		// setBadwords Метод установки списка плохих слов в список
		.def("setBadwords", overload_cast_ <const vector <wstring> &> ()(&anyks::Methods::setBadwords), "Method set words to blacklist", py::call_guard <py::gil_scoped_release>())
		// arabic2Roman Метод перевода арабских чисел в римские
		.def("arabic2Roman", overload_cast_ <const wstring &> ()(&anyks::Methods::arabic2Roman), "Convert arabic number to roman number", py::call_guard <py::gil_scoped_release>())
		// setGoodwords Метод установки списка идентификаторов хороших слов в список
		.def("setGoodwords", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setGoodwords), "Method set idw words to whitelist", py::call_guard <py::gil_scoped_release>())
		// setGoodwords Метод установки списка хороших слов в список
		.def("setGoodwords", overload_cast_ <const vector <wstring> &> ()(&anyks::Methods::setGoodwords), "Method set words to whitelist", py::call_guard <py::gil_scoped_release>())
		// countGrams Метод проверки количества найденных n-грамм
		.def("countGrams", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::countGrams), "Method get count N-gram by lm size", py::call_guard <py::gil_scoped_release>())
		// setSuffixes Метод установки списка идентификаторов аббревиатур
		.def("setSuffixes", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setSuffixes), "Method set number suffix abbreviations", py::call_guard <py::gil_scoped_release>())
		// isSuffix Метод проверки слова на суффикс цифровой аббревиатуры
		.def("isSuffix", overload_cast_ <const wstring &> ()(&anyks::Methods::isSuffix), "Checking a word against a number suffix abbreviation", py::call_guard <py::gil_scoped_release>())
		// getUppers Метод извлечения регистров для каждого слова
		.def("getUppers", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::getUppers), "Method for extracting registers for each word", py::call_guard <py::gil_scoped_release>())
		// check Метод проверки слова на существование его в словаре
		.def("check", overload_cast_ <const wstring &> ()(&anyks::Methods::check), "Method for checking a word for its existence in the dictionary", py::call_guard <py::gil_scoped_release>())
		// addUWord Метод добавления слова, которое всегда начинается с заглавной буквы
		.def("addUWord", overload_cast_ <const wstring &> ()(&anyks::Methods::addUWord), "Method for add a word that always starts with a capital letter", py::call_guard <py::gil_scoped_release>())
		// addUWord Метод добавления идентификатора слова, которое всегда начинается с заглавной буквы
		.def("addUWord", overload_cast_ <const size_t, const size_t> ()(&anyks::Methods::addUWord), "Method for add the ID of a word that always starts with a capital letter", py::call_guard <py::gil_scoped_release>());
	}{
		// setSize Метод установки размера n-граммы
		m.def("setSize", &anyks::Methods::setSize, "Method for set size N-gram", py::arg("size") = DEFNGRAM, py::call_guard <py::gil_scoped_release>())
		// buildArpa Метод сборки ARPA
		.def("buildArpa", &anyks::Methods::buildArpa, "Method for build ARPA", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// setLocale Метод установки локали
		.def("setLocale", &anyks::Methods::setLocale, "Method for set locale", py::arg("text") = "en_US.UTF-8", py::call_guard <py::gil_scoped_release>())
		// buildBloom Метод сборки фильтра Блума
		.def("buildBloom", &anyks::Methods::buildBloom, "Method for build Bloom filter", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// idw Метод извлечения идентификатора слова
		.def("idw", &anyks::Methods::idw, "Word ID retrieval method", py::arg("word") = L"", py::arg("check") = true, py::call_guard <py::gil_scoped_release>())
		// buildStemming Метод сборки стеммера
		.def("buildStemming", &anyks::Methods::buildStemming, "Method for build stemmer", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// setThreads Метод установки количества потоков
		.def("setThreads", &anyks::Methods::setThreads, "Method for set the number of threads", py::arg("threads") = 0, py::call_guard <py::gil_scoped_release>())
		// buildIndex Метод сборки индекса Спеллчекера
		.def("buildIndex", &anyks::Methods::buildIndex, "Method for build spell-checker index", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// word Метод извлечения слова по его идентификатору
		.def("word", &anyks::Methods::word, "Method to extract a word by its identifier", py::arg("idw") = 0, py::arg("ups") = 0, py::call_guard <py::gil_scoped_release>())
		// addText Метод добавления текста для расчёта
		.def("addText", &anyks::Methods::addText, "Method of adding text for estimate", py::arg("text") = "", py::arg("idd") = 0, py::call_guard <py::gil_scoped_release>())
		// setAdCw Метод установки характеристик словаря
		.def("setAdCw", &anyks::Methods::setAdCw, "Method for set dictionary characteristics", py::arg("cw") = 1, py::arg("ad") = 1, py::call_guard <py::gil_scoped_release>())
		// spell Метод выполнения исправления опечаток
		.def("spell", &anyks::Methods::spell, "A method of performing correction text", py::arg("text") = L"", py::arg("stat") = false, py::call_guard <py::gil_scoped_release>())
		// fti Метод удаления дробной части числа
		.def("fti", &anyks::Methods::fti, "Method for removing the fractional part of a number", py::arg("num") = 0.0, py::arg("count") = 0, py::call_guard <py::gil_scoped_release>())
		// readVocab Метод чтения словаря
		.def("readVocab", &anyks::Methods::readVocab, "Method of reading the dictionary", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// setNSWLibCount Метод установки максимального количества вариантов для анализа
		.def("setNSWLibCount", &anyks::Methods::setNSWLibCount, "Method for set the maximum number of options for analysis", py::arg("count") = 0, py::call_guard <py::gil_scoped_release>())
		// clear Метод очистки
		.def("clear", overload_cast_ <const anyks::clear_t> ()(&anyks::Methods::clear), "Method clear all data", py::arg("flag") = anyks::clear_t::all, py::call_guard <py::gil_scoped_release>())
		// writeArpa Метод записи данных в файл arpa
		.def("writeArpa", &anyks::Methods::writeArpa, "Method for writing data to an ARPA file", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// writeMap Метод записи карты последовательности в файл
		.def("writeMap", &anyks::Methods::writeMap, "Method for writing a sequence map to a file", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// writeWords Метод записи данных слов в файл
		.def("writeWords", &anyks::Methods::writeWords, "Method for writing these words to a file", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// addWord Метод добавления слова в словарь
		.def("addWord", &anyks::Methods::addWord, "Method for add a word to the dictionary", py::arg("word") = L"", py::arg("idw") = 0, py::arg("idd") = 0, py::call_guard <py::gil_scoped_release>())
		// writeNgrams Метод записи данных в файлы ngrams
		.def("writeNgrams", &anyks::Methods::writeNgrams, "Method for writing data to ngrams files", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// readArpa Метод чтения arpa файла, языковой модели
		.def("readArpa", &anyks::Methods::readArpa, "Method for reading an ARPA file, language model", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// writeVocab Метод записи данных словаря в файл
		.def("writeVocab", &anyks::Methods::writeVocab, "Method for writing dictionary data to a file", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// writeAbbrs Метод записи данных в файл аббревиатур
		.def("writeAbbrs", &anyks::Methods::writeAbbrs, "Method for writing data to an abbreviation file", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// context Метод сборки текстового контекста из последовательности
		.def("context", &anyks::Methods::context, "Method for assembling text context from a sequence", py::arg("seq") = vector <size_t> (), py::arg("nwrd") = false, py::call_guard <py::gil_scoped_release>())
		// pruneArpa Метод прунинга языковой модели
		.def("pruneArpa", &anyks::Methods::pruneArpa, "Language model pruning method", py::arg("threshold") = 0.0, py::arg("mingram") = 0, py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// findByFiles Метод поиска n-грамм в текстовом файле
		.def("findByFiles", &anyks::Methods::findByFiles, "Method search N-grams in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("ext") = L"txt", py::call_guard <py::gil_scoped_release>())
		// pruneVocab Метод прунинга словаря
		.def("pruneVocab", &anyks::Methods::pruneVocab, "Dictionary pruning method", py::arg("wltf") = 0.0, py::arg("oc") = 0, py::arg("dc") = 0, py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// pplByFiles Метод чтения расчёта перплексии по файлу или группе файлов
		.def("pplByFiles", &anyks::Methods::pplByFiles, "Method for reading perplexity calculation by file or group of files", py::arg("path") = L"", py::arg("ext") = L"txt", py::call_guard <py::gil_scoped_release>())
		// loadIndex Метод загрузки бинарного индекса
		.def("loadIndex", &anyks::Methods::loadIndex, "Method for loading spell-checker index", py::arg("filename") = "", py::arg("password") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// readSuffix Метод чтения данных из файла суффиксов цифровых аббревиатур
		.def("readSuffix", &anyks::Methods::readSuffix, "Method for reading data from a file of suffixes and abbreviations", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// writeSuffix Метод записи данных в файл суффиксов цифровых аббревиатур
		.def("writeSuffix", &anyks::Methods::writeSuffix, "Method for writing data to a suffix file for digital abbreviations", py::arg("filename") = "", py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const wstring &, const u_short> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("text") = L"", py::arg("step") = 2, py::call_guard <py::gil_scoped_release>())
		// existSequence Метод проверки существования последовательности, без учёта токенов не являющимися словами
		.def("existSequence", overload_cast_ <const wstring &, const u_short> ()(&anyks::Methods::existSequence), "Sequence Existence Method", py::arg("text") = L"", py::arg("step") = 2, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const wstring &, const bool> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("text") = L"", py::arg("accurate") = false, py::call_guard <py::gil_scoped_release>())
		// check Метод проверки строки
		.def("check", overload_cast_ <const wstring &, const anyks::check_t> ()(&anyks::Methods::check), "String Check Method", py::arg("str") = L"", py::arg("flag") = anyks::check_t::letter, py::call_guard <py::gil_scoped_release>())
		// sentencesToFile Метод сборки указанного количества предложений и записи в файл
		.def("sentencesToFile", &anyks::Methods::sentencesToFile, "Method for assembling a specified number of sentences and writing to a file", py::arg("counts") = 0, py::arg("filename") = L"", py::call_guard <py::gil_scoped_release>())
		// saveIndex Метод создания бинарного индекса
		.def("saveIndex", &anyks::Methods::saveIndex, "Method for save spell-checker index", py::arg("filename") = "", py::arg("password") = "", py::arg("aes") = 128, py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>())
		// match Метод проверки соответствия строки
		.def("match", overload_cast_ <const wstring &, const anyks::match_t> ()(&anyks::Methods::match), "String Matching Method", py::arg("str") = L"", py::arg("flag") = anyks::match_t::allowed, py::call_guard <py::gil_scoped_release>())
		// fixUppersByFiles Метод исправления регистров текста в текстовом файле
		.def("fixUppersByFiles", &anyks::Methods::fixUppersByFiles, "Method for correcting text registers in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("ext") = L"txt", py::call_guard <py::gil_scoped_release>())
		// tanimoto Метод определения коэффициента Жаккара (частное — коэф. Танимото)
		.def("tanimoto", &anyks::Methods::tanimoto, "Method for determining Jaccard coefficient (quotient - Tanimoto coefficient)", py::arg("first") = L"", py::arg("second") = L"", py::arg("stl") = 2, py::call_guard <py::gil_scoped_release>())
		// Метод добавления идентификатора суффикса цифровой аббреувиатуры
		.def("addSuffix", overload_cast_ <const wstring &, const size_t> ()(&anyks::Methods::addSuffix), "Method add number suffix abbreviation", py::arg("word") = L"", py::arg("idw") = anyks::idw_t::NIDW, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <size_t> &, const u_short> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <size_t> (), py::arg("step") = 2, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности, без учёта токенов не являющимися словами
		.def("existSequence", overload_cast_ <const vector <size_t> &, const u_short> ()(&anyks::Methods::existSequence), "Sequence Existence Method", py::arg("seq") = vector <size_t> (), py::arg("step") = 2, py::call_guard <py::gil_scoped_release>())
		// needlemanWunsch Метод натяжения слов
		.def("needlemanWunsch", &anyks::Methods::needlemanWunsch, "Word stretching method", py::arg("first") = L"", py::arg("second") = L"", py::arg("match") = 1, py::arg("mismatch") = -1, py::arg("gap") = -2, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <wstring> &, const u_short> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <wstring> (), py::arg("step") = 2, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности, без учёта токенов не являющимися словами
		.def("existSequence", overload_cast_ <const vector <wstring> &, const u_short> ()(&anyks::Methods::existSequence), "Sequence Existence Method", py::arg("seq") = vector <wstring> (), py::arg("step") = 2, py::call_guard <py::gil_scoped_release>())
		// delInText Метод очистки текста
		.def("delInText", overload_cast_ <const wstring &, const anyks::wdel_t> ()(&anyks::Methods::delInText), "Method for delete letter in text", py::arg("text") = L"", py::arg("flag") = anyks::wdel_t::broken, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <size_t> &, const bool> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <size_t> (), py::arg("accurate") = false, py::call_guard <py::gil_scoped_release>())
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <size_t> &, const bool> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <wstring> (), py::arg("accurate") = false, py::call_guard <py::gil_scoped_release>())
		// countsByFiles Метод подсчёта количества n-грамм в текстовом файле
		.def("countsByFiles", &anyks::Methods::countsByFiles, "Method for counting the number of n-grams in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("ngrams") = 0, py::arg("ext") = L"txt", py::call_guard <py::gil_scoped_release>())
		// checkByFiles Метод проверки существования последовательности в текстовом файле
		.def("checkByFiles", &anyks::Methods::checkByFiles, "Method for checking if a sequence exists in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("accurate") = false, py::arg("ext") = L"txt", py::call_guard <py::gil_scoped_release>())
		// addAlt Метод добавления слова с альтернативной буквой
		.def("addAlt", overload_cast_ <const string &, const string &, const bool> ()(&anyks::Methods::addAlt), "Method for add a word with an alternative letter", py::arg("word") = "", py::arg("alt") = "", py::arg("context") = false, py::call_guard <py::gil_scoped_release>())
		// addAlt Метод добавления слова с альтернативной буквой
		.def("addAlt", overload_cast_ <const wstring &, const size_t, const bool> ()(&anyks::Methods::addAlt), "Method for add a word with an alternative letter", py::arg("word") = L"", py::arg("idw") = anyks::idw_t::NIDW,  py::arg("context") = false, py::call_guard <py::gil_scoped_release>())
		// collectCorpus Метод обучения сборки текстовых данных Спеллчекера
		.def("collectCorpus", &anyks::Methods::collectCorpus, "Training method of assembling the text data for Spell-checker", py::arg("corpus") = L"", py::arg("smoothing") = anyks::smoothing_t::wittenBell, py::arg("mod") = 0.0, py::arg("modified") = false, py::arg("prepares") = false, py::arg("status") = nullptr, py::call_guard <py::gil_scoped_release>());
	}
};

#endif // _ANYKS_SC_
