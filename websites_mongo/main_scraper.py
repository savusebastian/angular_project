from scraper_1cctv import f1cctv_DB
from scraper_3gifts import f3gifts_DB
# from scraper_3pitici import f3pitici_DB # Au dat ban pe ip
# from scraper_abdcomputer import abdcomputer_DB # Au dat ban pe ip
from scraper_alecoair import alecoair_DB
from scraper_allview import allview_DB
from scraper_aloshop import aloshop_DB
from scraper_animax import animax_DB
from scraper_apiland import apiland_DB
from scraper_artofplay import artofplay_DB
from scraper_autoeco import autoeco_DB
# from scraper_autohut import autohut_DB
from scraper_automobilus import automobilus_DB
from scraper_avmall import avmall_DB
from scraper_b_mall import b_mall_DB
from scraper_babyliss_romania import babyliss_romania_DB
from scraper_bagno import bagno_DB
from scraper_benvenuti import benvenuti_DB
from scraper_bestkids import bestkids_DB
from scraper_bioboom import bioboom_DB
from scraper_borealy import borealy_DB
from scraper_carnaval24 import carnaval24_DB
from scraper_cartepedia import cartepedia_DB
from scraper_case_smart import case_smart_DB
from scraper_cel import cel_DB
# from scraper_citgrup import citgrup_DB
# from scraper_cleste import cleste_DB
from scraper_colorcosmetics import colorcosmetics_DB
from scraper_crockpot_romania import crockpot_romania_DB
from scraper_delamamici import delamamici_DB
from scraper_divahome import divahome_DB
from scraper_divisima import divisima_DB
from scraper_domo import domo_DB
from scraper_dwyn import dwyn_DB
from scraper_e_pneus import e_pneus_DB
from scraper_educlass import educlass_DB
from scraper_emag import emag_DB
from scraper_emobili import emobili_DB
from scraper_enbook import enbook_DB
from scraper_enzobertini import enzobertini_DB
# from scraper_erotic24 import erotic24_DB # Au dat ban pe ip
from scraper_eugfashion import eugfashion_DB
from scraper_evomag import evomag_DB
from scraper_fara_daunatori import fara_daunatori_DB
from scraper_fashion_24 import fashion_24_DB
from scraper_fashionagenda import fashionagenda_DB
from scraper_fashiondays import fashiondays_DB
from scraper_flanco import flanco_DB
from scraper_floridelux import floridelux_DB
from scraper_gadgetway import gadgetway_DB
from scraper_generalmotor import generalmotor_DB
from scraper_giftforyou import giftforyou_DB
from scraper_graveazaiubirea import graveazaiubirea_DB
from scraper_haircare import haircare_DB
from scraper_henderson import henderson_DB
from scraper_horolonger import horolonger_DB
from scraper_iconicul import iconicul_DB
from scraper_ihunt import ihunt_DB
from scraper_inpuff import inpuff_DB
# from scraper_isayaa import isayaa_DB
from scraper_itgalaxy import itgalaxy_DB
from scraper_kinghoff import kinghoff_DB
from scraper_kurtmann import kurtmann_DB
from scraper_lensa import lensa_DB
from scraper_lentiamo import lentiamo_DB
from scraper_libris import libris_DB
from scraper_lomeye import lomeye_DB
from scraper_mannasapun import mannasapun_DB
from scraper_market365 import market365_DB
from scraper_maxlife import maxlife_DB
from scraper_megaplus import megaplus_DB
from scraper_melkior import melkior_DB
from scraper_military_shop import military_shop_DB
from scraper_mindblower import mindblower_DB
from scraper_mycloset import mycloset_DB
from scraper_neer import neer_DB
from scraper_nemira import nemira_DB
from scraper_nuiorganics import nuiorganics_DB
from scraper_partymag import partymag_DB
from scraper_pcgarage import pcgarage_DB
from scraper_pchouse import pchouse_DB
from scraper_pcmadd import pcmadd_DB
from scraper_pcmall import pcmall_DB
from scraper_pellamar import pellamar_DB
from scraper_perfectbijoux import perfectbijoux_DB
from scraper_piesemotor import piesemotor_DB
from scraper_piticulvesel import piticulvesel_DB
from scraper_pufo import pufo_DB
from scraper_rangali import rangali_DB
from scraper_remediu import remediu_DB
from scraper_rubyfashion import rubyfashion_DB
from scraper_sangado import sangado_DB
from scraper_scufita_rosie import scufita_rosie_DB
from scraper_scutecila import scutecila_DB
from scraper_sevensins import sevensins_DB
from scraper_shopperfectpet import shopperfectpet_DB
from scraper_shopu import shopu_DB
from scraper_smart_products import smart_products_DB
from scraper_sportpartner import sportpartner_DB
from scraper_steaua_divina import steaua_divina_DB
from scraper_stickere import stickere_DB
from scraper_stifler import stifler_DB
from scraper_techstar import techstar_DB
from scraper_topwatch import topwatch_DB
from scraper_totalcomenzi import totalcomenzi_DB
from scraper_upcar import upcar_DB
from scraper_vegis import vegis_DB
# from scraper_vesa import vesa_DB 403 forbidden
from scraper_vexio import vexio_DB
from scraper_vonino import vonino_DB
from scraper_vonmag import vonmag_DB
from scraper_want import want_DB
from scraper_watch24 import watch24_DB
from scraper_watchshop import watchshop_DB
from scraper_watchzone import watchzone_DB
from scraper_xtdeco import xtdeco_DB
from time import time
import multiprocessing


if __name__ == '__main__':
	start_time = time()
	fns = [
		flanco_DB, f1cctv_DB, alecoair_DB,
		aloshop_DB, animax_DB, avmall_DB, babyliss_romania_DB,
		bagno_DB, benvenuti_DB, borealy_DB, case_smart_DB,
		crockpot_romania_DB, delamamici_DB, divahome_DB, dwyn_DB, educlass_DB,
		enzobertini_DB, eugfashion_DB, fara_daunatori_DB, fashionagenda_DB,
		generalmotor_DB, giftforyou_DB, graveazaiubirea_DB, haircare_DB, henderson_DB,
		horolonger_DB, ihunt_DB, inpuff_DB, lensa_DB, lentiamo_DB,
		lomeye_DB, mannasapun_DB, market365_DB, maxlife_DB, melkior_DB,
		mindblower_DB, neer_DB, nemira_DB, partymag_DB, pchouse_DB,
		piticulvesel_DB, rangali_DB, scutecila_DB, sevensins_DB, steaua_divina_DB,
		stickere_DB, stifler_DB, techstar_DB, upcar_DB, vegis_DB, vexio_DB,
		vonino_DB, vonmag_DB, watch24_DB, watchshop_DB, watchzone_DB,
	]
	processes = []

	for fn in fns:
		p = multiprocessing.Process(target=fn)
		p.start()
		processes.append(p)

	for p in processes:
		p.join()

	print('Ready:', (time() - start_time) / 3600)
