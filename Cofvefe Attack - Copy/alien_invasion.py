import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
	# Initializes the game and creates a screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Covfefe Attack! Adjust screen BEFORE press'PLAY'")
	# Make the play button
	play_button = Button(ai_settings, screen, "Play")
	
	# Create an instance to store game statistics and create a scoreboard
	stats = GameStats(ai_settings)	
	sb = Scoreboard(ai_settings, screen, stats)
	# Make ship, a group of bullets, ad a group of aliens
	ship = Ship(ai_settings, screen)
	# Make a group to store bullets in
	bullets = Group()
	# Make a group to store alien invaders
	aliens = Group()
	# Create a fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# Start the main loop for the game.
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
			aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, 
				bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, 
				bullets)
			
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
			bullets, play_button)  		
		
run_game()	

