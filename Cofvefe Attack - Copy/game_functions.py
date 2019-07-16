import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses"""
	if event.key == pygame.K_RIGHT:
		# Move ship to the right
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		# Move ship to the left
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
		
def fire_bullet(ai_settings, screen, ship, bullets):
	"""fire a bullet if limit not reached yet"""		
	# Create a new bullet and add it to bullets Group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

# don't need to change keyup_events
		
def check_keyup_events(event, ship):
	"""Respond to key releases"""
	if event.key == pygame.K_RIGHT:
		# Move ship to the right
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		# Move ship to the left
		ship.moving_left = False	
		
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
		bullets):
	"""Respond to keypresses and mouse events."""
	 # Watch for keyboard and mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			#Begin moving ship to the left
			check_keydown_events(event, ai_settings, screen, ship, 
				bullets)
		elif event.type == pygame.KEYUP:
			# Stopship to the left
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y, = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, 
				ship, aliens, bullets, mouse_x, mouse_y)
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
		aliens, bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks PLAY."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game settings
		#ai_settings.initialize_dynamic_settings()
		
		# Hide the mouse cursor
		pygame.mouse.set_visible(False)
		# Reset game statistics
		stats.reset_stats()
		stats.game_active = True
		
		# Reset the scoreboard language
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# Empty list of alins and bullets
		aliens.empty()
		bullets.empty()
		
		# Create a new fleet and center the ship 
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()	
			
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
		play_button):
	"""Update images on the screen and flip to new screen"""
	# Redraw the screen during each pass of the loop
	screen.fill(ai_settings.bg_color)
	# Redraw all bullets behind sprites and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	# Draw the scoreboard information
	sb.show_score()
	
	# Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
								
	# Make the most recently drawn screen visible. 
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Update position of bullets and get rid of old bullets"""
	# Update bullet position
	bullets.update()	
	# Get rid of old bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	# Check for bullets that hit aliens
	# If so, get rid of both alien and bullet
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
		aliens, bullets) 
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
		 aliens, bullets):
	"""Respond to bullet-alien collisions"""
	# Remove any bullets and aliens that have collided
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()	
		check_high_score(stats, sb)
	if len(aliens) == 0:
		# If entre fleet is destroyed, start a new level
		# Destroy existing bullets, speed up game, and create new fleet
		bullets.empty()
		ai_settings.increase_speed()
		
		# Increase level
		stats.level += 1
		sb.prep_level()
		
		# Recreate fleet and shipafter clear, and reset position
		create_fleet(ai_settings, screen, ship, aliens)
			
def get_number_aliens_x(ai_settings, alien_width):
	"""Determine number of aliens that fit in row"""
	available_space_x = ai_settings.screen_width - 1.5 * alien_width
	number_aliens_x = int(available_space_x / (1.5 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of alien ships"""
	available_space_y = (ai_settings.screen_height - 
							(2.5 * alien_height) - ship_height)
	number_rows = int(available_space_y / (1.5 * alien_height))
	#change constant 1.6 to 2 for easier game in g_n_r() and c_a()
	return number_rows
		
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and places it in a row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 1.5 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
	aliens.add(alien)
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full alien fleet"""
	#Create an alien and find the number of aliens in a row
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, 
		alien.rect.height)
	
	# Create the fleet of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,	
				row_number)
				
def check_fleet_edges(ai_settings, aliens):
	"""Respond apropo if alien reaches edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop the fleet and change its direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""respond to ship being hit by an alien"""
	if stats.ships_left > 0:
		# Decrement ship left
		stats.ships_left -= 1
		
		# Update scoreboard
		sb.prep_ships()
	
		# Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
	
		# Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		# Pause.
		sleep(0.5)
	
	else:
		 stats.game_active = False
		 pygame.mouse.set_visible(True)
		
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
		bullets):
	"""Check if aliens have reached the bottom of the sscreen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this event as the same thing as a collision
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break	
	
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check for fleet edge, update nearbys in fleet"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()	
	# Look for alien-ship collisionsif pygame.sprite.spritecollideany(ship, aliens):
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
		print ("Covfefe!!!")
	# Look for aliens hitting bottom of screen
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
def check_high_score(stats, sb):
	"""check to see if there is a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
