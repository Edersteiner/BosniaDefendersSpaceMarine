import kaiserengine.engine as engine
import random

class Space:
    def __init__(self):
        self.game = engine.init(1280, 720, "Bosnia Defenders Space Marine: DeluXe Edition 1991 Game of the Year", "assets/ship/ship0.png")
        self.game.fullscreen(engine.keys.KEY_F)

        self.game.cooldown(100, "Shoot Cooldown")
        self.game.cooldown(150, "Shoot Cooldown 2")
        self.game.cooldown(1300, "Missile Cooldown")
        self.game.cooldown(15000, "Powerup Cooldown")
        self.game.cooldown(10000, "Beam Duration")

        self.beam_powerup = False
        self.active_powerupbox = False
        self.active_powerup = False

        self.beambox = None

        self.projectiles = []
        self.missiles = []
        self.game_missiles = 0
        self.score = 0

    def destroy_missile(self, hitname):
        missile = self.game.find_sprite(hitname)
        self.game.particle_effect(missile.sprite_x + missile.sprite_w/2, missile.sprite_y + missile.sprite_h/2, 20, 0.1, 20, (26, 26, 24))
        self.game.particle_effect(missile.sprite_x + missile.sprite_w/2, missile.sprite_y + missile.sprite_h/2, 5, 0.06, 130, (255, 144, 35))
        self.game.particle_effect(missile.sprite_x + missile.sprite_w/2, missile.sprite_y + missile.sprite_h/2, 5, 0.08, 190, (255, 244, 35))

        missile.destroy()
        self.missiles.remove(missile)
        del missile

        self.game.audio_controller.play_sfx("assets/explosion.mp3", 10)

    def update(self):
        if self.game.controller.pressed(engine.keys.KEY_W):
            self.player.move_y((int(self.game.delta_time * 0.60)))
        if self.game.controller.pressed(engine.keys.KEY_D):
            self.player.move_x((int(self.game.delta_time * 0.60)))
        if self.game.controller.pressed(engine.keys.KEY_S):
            self.player.move_y(-(int(self.game.delta_time * 0.60)))
        if self.game.controller.pressed(engine.keys.KEY_A):
            self.player.move_x(-(int(self.game.delta_time * 0.60)))

        if self.game.find_cooldown("Missile Cooldown").status() == 1:
            current_missile = self.game.sprite(self.game.find_image("Missile"), random.randrange(40, 1240), -200, 28, 100, "Missile " + str(self.game_missiles))
            current_missile.bitmap_set(self.game.find_image("Missile"))
            self.missiles.append(current_missile)
            self.game_missiles += 1

        if self.active_powerupbox == False:
            if self.game.find_cooldown("Powerup Cooldown").status() == 1:
                powerup = random.randrange(0, 2)
                
                if powerup == 1:
                    self.beambox = self.game.sprite(self.game.find_image("Beambox"), random.randrange(50, 1230), random.randrange(100, 500), 58, 86, "Beambox")
                    self.beambox.bitmap_timing(30)
                    self.active_powerupbox = True
                    
        if self.game.find_cooldown("Beam Duration").status() == 1:
            self.beam_powerup = False
            self.active_powerup = False


        if self.game.controller.pressed(engine.keys.KEY_SPACE):
                if self.beam_powerup == True:
                    projectile = self.game.projectile(self.player.mid(0) - 19, self.player.mid(1)+45, 0, -710, 40, 40, 0.01 * self.game.delta_time, (99, 155, 255))
                    projectile.bitmap_set(self.game.find_image("Beam"))
                    self.projectiles.append(projectile)
                else:
                    if self.game.find_cooldown("Shoot Cooldown").status() == 1:
                        projectile = self.game.projectile(self.player.mid(0)+25, self.player.mid(1)+57, 0, -710, 8, 16, 0.01 * self.game.delta_time, (99, 155, 255))
                        projectile.bitmap_set(self.game.find_image("Bullet"))
                        self.projectiles.append(projectile)

                    if self.game.find_cooldown("Shoot Cooldown 2").status() == 1:
                        projectile = self.game.projectile(self.player.mid(0)-25, self.player.mid(1)+57, 0, -710, 8, 16, 0.01 * self.game.delta_time, (99, 155, 255))
                        projectile.bitmap_set(self.game.find_image("Bullet"))
                        self.projectiles.append(projectile)

            

        if len(self.missiles) > 0:
            for missile in self.missiles:
                missile.move_y(-int(self.game.delta_time * 0.2))
                if missile.sprite_y > 580:
                    self.destroy_missile(missile.sprite_n)
                    self.player_health_bar.rec_w -= 20

        player_collided = self.player.collided()
        if player_collided:
            if "Missile" in player_collided:
                self.destroy_missile(player_collided)
                if self.player_health_bar.rec_w-20 <= 0:
                    print("Game Over")
                    self.game.is_running = False
                self.player_health_bar.rec_w -= 20
            if "Beambox" in player_collided:
                self.game.find_cooldown("Beam Duration").reset()
                hit_beambox = self.game.find_sprite("Beambox")
                self.game.particle_effect(hit_beambox.mid(0), hit_beambox.mid(1) + hit_beambox.sprite_y / 4, 5, 0.06, 130, (129, 178, 245))
                self.game.particle_effect(hit_beambox.mid(0), hit_beambox.mid(1) + hit_beambox.sprite_y / 4, 5, 0.08, 190, (233, 242, 255))

                hit_beambox.destroy()
                self.active_powerupbox = False
                self.beam_powerup = True

        if len(self.projectiles) > 0:
            for projectile in self.projectiles:
                hitname = str(projectile.hit())
                if "Missile" in hitname and projectile.projectile_cy > 5:
                    self.destroy_missile(hitname)
                    self.projectiles.remove(projectile)
                    self.score += 10
                    self.score_text.text("Score: " + str(self.score))

    def run(self):
        self.game.fps = 60
        self.game.audio_controller.set("assets/pinball.mp3")
        self.game.audio_controller.volume(10)
        self.game.audio_controller.play()


        self.game.load_image("assets/missile.ivan", "Missile")
        self.game.load_image("assets/bullet.png", "Bullet")
        self.game.load_image("assets/beam.png", "Beam")
        self.game.load_image("assets/beambox.ivan", "Beambox")
        self.game.set_background("assets/space.png")

        self.player = self.game.sprite("assets/ship.ivan", 600, 200, 75, 79, "Player")
        self.player.bitmap_timing(20)

        # UI
        self.player_health_bar = self.game.rectangle(10, 10, 200, 10, engine.colors.WHITE, static=True)
        self.game.font("Arial", 20)
        self.score_text = self.game.text("Score: 0", 1180, 10, engine.colors.WHITE)  

        self.player.screen_boundary = True
        self.game.task(self.update, "Update")
        self.game.run()

g = Space()
g.run()
