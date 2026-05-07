from controller import Robot

MAX_SPEED = 6.28
THRESHOLD = 80.0
TIEMPO_GIRO = 15

def run():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    sensor_names = ["ps0","ps1","ps2","ps3","ps4","ps5","ps6","ps7"]
    sensors = []
    for name in sensor_names:
        sensor = robot.getDevice(name)
        sensor.enable(timestep)
        sensors.append(sensor)

    contador_giro = 0
    girando_derecha = True

    while robot.step(timestep) != -1:
        valores = [s.getValue() for s in sensors]

        frente_der = valores[0]
        frente_izq = valores[7]
        lado_der = max(valores[1], valores[2])
        lado_izq = max(valores[5], valores[6])

        obstaculo_frente = frente_der > THRESHOLD or frente_izq > THRESHOLD
        obstaculo_der = lado_der > THRESHOLD
        obstaculo_izq = lado_izq > THRESHOLD

        if contador_giro > 0:
            if girando_derecha:
                left_motor.setVelocity(MAX_SPEED * 0.6)
                right_motor.setVelocity(-MAX_SPEED * 0.6)
            else:
                left_motor.setVelocity(-MAX_SPEED * 0.6)
                right_motor.setVelocity(MAX_SPEED * 0.6)
            contador_giro -= 1

        elif obstaculo_frente:
            if frente_der > frente_izq:
                girando_derecha = False
                left_motor.setVelocity(-MAX_SPEED * 0.5)
                right_motor.setVelocity(MAX_SPEED * 0.5)
            else:
                girando_derecha = True
                left_motor.setVelocity(MAX_SPEED * 0.5)
                right_motor.setVelocity(-MAX_SPEED * 0.5)
            contador_giro = TIEMPO_GIRO

        elif obstaculo_der and not obstaculo_izq:
            left_motor.setVelocity(MAX_SPEED * 0.3)
            right_motor.setVelocity(MAX_SPEED * 0.8)

        elif obstaculo_izq and not obstaculo_der:
            left_motor.setVelocity(MAX_SPEED * 0.8)
            right_motor.setVelocity(MAX_SPEED * 0.3)

        else:
            left_motor.setVelocity(MAX_SPEED)
            right_motor.setVelocity(MAX_SPEED)

run()
