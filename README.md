# Embudo-de-eventos-y-test-A-A-B
Los usuarios se dividen en tres grupos: dos grupos de control obtienen las fuentes antiguas y un grupo de prueba obtiene las nuevas. Descubre qué conjunto de fuentes produce mejores resultados.
<img width="774" height="699" alt="Captura de pantalla 2026-02-12 005229" src="https://github.com/user-attachments/assets/02c46982-da9c-4876-a792-b8e7ed4fa2b0" />
<img width="837" height="275" alt="Captura de pantalla 2026-02-12 005237" src="https://github.com/user-attachments/assets/d037a831-a27e-45cb-a903-6889692c0879" />
<img width="788" height="693" alt="Captura de pantalla 2026-02-12 005310" src="https://github.com/user-attachments/assets/b8850dfb-add0-4ce0-a2bf-495d7d9ce70c" />


numero de evento a:4201
numero de evento b: 1767
numero de evento c: 454
proporcion de B respecto a A: 42.06141394905975
proporcion de C respecto a B: 25.693265421618563
Por lo que se puede apreciar se ve que en la etapa C se pierde una cantidad sigmificativa de usarios

Distribución de usuarios:
Grupo 246: 2489 usuarios (33.0%)
Grupo 247: 2520 usuarios (33.4%)
Grupo 248: 2542 usuarios (33.7%)

Todos los eventos:
                    evento  usuarios_246  usuarios_247  proporcion_246  \
4  PaymentScreenSuccessful          1200          1158        0.483092   
3         CartScreenAppear          1266          1238        0.509662   
2       OffersScreenAppear          1542          1520        0.620773   
1         MainScreenAppear          2450          2476        0.986312   
0                 Tutorial           278           283        0.111916   

   proporcion_247    pvalue  
4        0.460804  0.114567  
3        0.492638  0.228834  
2        0.604855  0.248095  
1        0.985277  0.757060  
0        0.112614  0.937700  
no hay grupos que tengan diferencias sigmificatias, asi que se puede confirmar que se dividieron bien.

comparacion del grupo 246                     evento  usuarios_experimental  usuarios_control_246  \
0                 Tutorial                    279                   278   
1         MainScreenAppear                   2493                  2450   
2       OffersScreenAppear                   1531                  1542   
3         CartScreenAppear                   1230                  1266   
4  PaymentScreenSuccessful                   1181                  1200   

   proporcion_experimental  proporcion_control_246    pvalue  
0                 0.109972                0.111916  0.826429  
1                 0.982657                0.986312  0.294972  
2                 0.603469                0.620773  0.208362  
3                 0.484825                0.509662  0.078429  
4                 0.465510                0.483092  0.212255  
comparacion del grupo 247                     evento  usuarios_experimental  usuarios_control_247  \
0                 Tutorial                    279                   283   
1         MainScreenAppear                   2493                  2476   
2       OffersScreenAppear                   1531                  1520   
3         CartScreenAppear                   1230                  1238   
4  PaymentScreenSuccessful                   1181                  1158   

   proporcion_experimental  proporcion_control_247    pvalue  
0                 0.109972                0.112614  0.765324  
1                 0.982657                0.985277  0.458705  
2                 0.603469                0.604855  0.919782  
3                 0.484825                0.492638  0.578620  
4                 0.465510                0.460804  0.737342  
comparacion del grupo combinado                     evento  usuarios_experimental  usuarios_control_777  \
0                 Tutorial                    279                   561   
1         MainScreenAppear                   2493                  4926   
2       OffersScreenAppear                   1531                  3062   
3         CartScreenAppear                   1230                  2504   
4  PaymentScreenSuccessful                   1181                  2358   

   proporcion_experimental  proporcion_control_777    pvalue  
0                 0.109972                0.112267  0.764862  
1                 0.982657                0.985791  0.294245  
2                 0.603469                0.612768  0.434255  
3                 0.484825                0.501101  0.181759  
4                 0.465510                0.471883  0.600429  
los grupos de control no difieren sigmificamente entre si, lo que valida que el test es un exito y no se encontro diferencias sigmificativas en el grupo experimental

pruebas de hipótesis estadísticas realizadas: 15
0    False
1    False
2    False
3    False
4    False
Name: sigmificancia, dtype: bool
0    False
1    False
2    False
3    False
4    False
Name: sigmificancia, dtype: bool
0    False
1    False
2    False
3    False
4    False
Name: sigmificancia, dtype: bool
utilize el nivel de sigmificancia de 0.05 por defecto, pienso que el nivel de sigmificancia puede variar ya que 0.05 esta muy bien y da mas flexividad y so es 0.01 es un poco mas estricto que no se requirio en estas pruebas


