# SnowPeak: Distributed Ski Resort Monitoring System
A distributed system for real-time monitoring and control of ski resort lifts.




2024-11-11 22:59:40
2024-11-11 22:59:40   .   ____          _            __ _ _
2024-11-11 22:59:40  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
2024-11-11 22:59:40 ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
2024-11-11 22:59:40  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
2024-11-11 22:59:40   '  |____| .__|_| |_|_| |_\__, | / / / /
2024-11-11 22:59:40  =========|_|==============|___/=/_/_/_/
2024-11-11 22:59:40
2024-11-11 22:59:40  :: Spring Boot ::                (v3.3.5)
2024-11-11 22:59:40
2024-11-11 22:59:40 2024-11-11T21:59:40.834Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : Starting SnowPeakServerApplication v0.0.1-SNAPSHOT using Java 21.0.5 with PID 1 (/opt/app/app.jar started by spring in /opt/app)
2024-11-11 22:59:40 2024-11-11T21:59:40.837Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : No active profile set, falling back to 1 default profile: "default"
2024-11-11 22:59:42 2024-11-11T21:59:42.483Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2024-11-11 22:59:42 2024-11-11T21:59:42.574Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 78 ms. Found 2 JPA repository interfaces.
2024-11-11 22:59:43 2024-11-11T21:59:43.691Z  INFO 1 --- [snow-peak-server] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8080 (http)
2024-11-11 22:59:43 2024-11-11T21:59:43.712Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2024-11-11 22:59:43 2024-11-11T21:59:43.712Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.31]
2024-11-11 22:59:43 2024-11-11T21:59:43.765Z  INFO 1 --- [snow-peak-server] [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2024-11-11 22:59:43 2024-11-11T21:59:43.766Z  INFO 1 --- [snow-peak-server] [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 2865 ms
2024-11-11 22:59:44 2024-11-11T21:59:44.279Z  WARN 1 --- [snow-peak-server] [           main] com.zaxxer.hikari.HikariConfig           : HikariPool-1 - idleTimeout has been set but has no effect because the pool is operating as a fixed size pool.
2024-11-11 22:59:44 2024-11-11T21:59:44.281Z  INFO 1 --- [snow-peak-server] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2024-11-11 22:59:45 2024-11-11T21:59:45.360Z  WARN 1 --- [snow-peak-server] [           main] ConfigServletWebServerApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource [org/springframework/boot/autoconfigure/orm/jpa/HibernateJpaConfiguration.class]: Failed to initialize dependency 'flywayInitializer' of LoadTimeWeaverAware bean 'entityManagerFactory': Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:45 SQL State  : 08001
2024-11-11 22:59:45 Error Code : 0
2024-11-11 22:59:45 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45
2024-11-11 22:59:45 2024-11-11T21:59:45.363Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardService   : Stopping service [Tomcat]
2024-11-11 22:59:45 2024-11-11T21:59:45.376Z  INFO 1 --- [snow-peak-server] [           main] .s.b.a.l.ConditionEvaluationReportLogger :
2024-11-11 22:59:45
2024-11-11 22:59:45 Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2024-11-11 22:59:45 2024-11-11T21:59:45.406Z ERROR 1 --- [snow-peak-server] [           main] o.s.boot.SpringApplication               : Application run failed
2024-11-11 22:59:45
2024-11-11 22:59:45 org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource [org/springframework/boot/autoconfigure/orm/jpa/HibernateJpaConfiguration.class]: Failed to initialize dependency 'flywayInitializer' of LoadTimeWeaverAware bean 'entityManagerFactory': Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:45 SQL State  : 08001
2024-11-11 22:59:45 Error Code : 0
2024-11-11 22:59:45 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:326) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:205) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:954) ~[spring-context-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:625) ~[spring-context-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:146) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:754) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:456) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at org.springframework.boot.SpringApplication.run(SpringApplication.java:335) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at org.springframework.boot.SpringApplication.run(SpringApplication.java:1363) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at org.springframework.boot.SpringApplication.run(SpringApplication.java:1352) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at hu.snowpeak.server.SnowPeakServerApplication.main(SnowPeakServerApplication.java:10) ~[!/:0.0.1-SNAPSHOT]
2024-11-11 22:59:45 at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at java.base/java.lang.reflect.Method.invoke(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at org.springframework.boot.loader.launch.Launcher.launch(Launcher.java:102) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:45 at org.springframework.boot.loader.launch.Launcher.launch(Launcher.java:64) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:45 at org.springframework.boot.loader.launch.JarLauncher.main(JarLauncher.java:40) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:45 Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:45 SQL State  : 08001
2024-11-11 22:59:45 Error Code : 0
2024-11-11 22:59:45 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1806) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:600) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:522) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:337) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:335) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:200) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:313) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 ... 15 common frames omitted
2024-11-11 22:59:45 Caused by: org.flywaydb.core.internal.exception.FlywaySqlException: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:45 SQL State  : 08001
2024-11-11 22:59:45 Error Code : 0
2024-11-11 22:59:45 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45
2024-11-11 22:59:45 at org.flywaydb.core.internal.jdbc.JdbcUtils.openConnection(JdbcUtils.java:60) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:45 at org.flywaydb.core.internal.jdbc.JdbcConnectionFactory.<init>(JdbcConnectionFactory.java:72) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:45 at org.flywaydb.core.FlywayExecutor.execute(FlywayExecutor.java:134) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:45 at org.flywaydb.core.Flyway.migrate(Flyway.java:147) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:45 at org.springframework.boot.autoconfigure.flyway.FlywayMigrationInitializer.afterPropertiesSet(FlywayMigrationInitializer.java:66) ~[spring-boot-autoconfigure-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1853) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1802) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:45 ... 22 common frames omitted
2024-11-11 22:59:45 Caused by: org.postgresql.util.PSQLException: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:45 at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:352) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:54) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:273) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.Driver.makeConnection(Driver.java:446) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.Driver.connect(Driver.java:298) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at com.zaxxer.hikari.util.DriverDataSource.getConnection(DriverDataSource.java:137) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at com.zaxxer.hikari.pool.PoolBase.newConnection(PoolBase.java:360) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at com.zaxxer.hikari.pool.PoolBase.newPoolEntry(PoolBase.java:202) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:461) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at com.zaxxer.hikari.pool.HikariPool.checkFailFast(HikariPool.java:550) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at com.zaxxer.hikari.pool.HikariPool.<init>(HikariPool.java:98) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at com.zaxxer.hikari.HikariDataSource.getConnection(HikariDataSource.java:111) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:45 at org.flywaydb.core.internal.jdbc.JdbcUtils.openConnection(JdbcUtils.java:48) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:45 ... 28 common frames omitted
2024-11-11 22:59:45 Caused by: java.net.ConnectException: Connection refused
2024-11-11 22:59:45 at java.base/sun.nio.ch.Net.pollConnect(Native Method) ~[na:na]
2024-11-11 22:59:45 at java.base/sun.nio.ch.Net.pollConnectNow(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at java.base/sun.nio.ch.NioSocketImpl.timedFinishConnect(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at java.base/sun.nio.ch.NioSocketImpl.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at java.base/java.net.SocksSocketImpl.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at java.base/java.net.Socket.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:45 at org.postgresql.core.PGStream.createSocket(PGStream.java:260) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.core.PGStream.<init>(PGStream.java:121) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.core.v3.ConnectionFactoryImpl.tryConnect(ConnectionFactoryImpl.java:140) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:268) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:45 ... 40 common frames omitted
2024-11-11 22:59:45
2024-11-11 22:59:47
2024-11-11 22:59:47   .   ____          _            __ _ _
2024-11-11 22:59:47  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
2024-11-11 22:59:47 ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
2024-11-11 22:59:47  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
2024-11-11 22:59:47   '  |____| .__|_| |_|_| |_\__, | / / / /
2024-11-11 22:59:47  =========|_|==============|___/=/_/_/_/
2024-11-11 22:59:47
2024-11-11 22:59:47  :: Spring Boot ::                (v3.3.5)
2024-11-11 22:59:47
2024-11-11 22:59:47 2024-11-11T21:59:47.555Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : Starting SnowPeakServerApplication v0.0.1-SNAPSHOT using Java 21.0.5 with PID 1 (/opt/app/app.jar started by spring in /opt/app)
2024-11-11 22:59:47 2024-11-11T21:59:47.558Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : No active profile set, falling back to 1 default profile: "default"
2024-11-11 22:59:49 2024-11-11T21:59:49.145Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2024-11-11 22:59:49 2024-11-11T21:59:49.248Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 88 ms. Found 2 JPA repository interfaces.
2024-11-11 22:59:50 2024-11-11T21:59:50.327Z  INFO 1 --- [snow-peak-server] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8080 (http)
2024-11-11 22:59:50 2024-11-11T21:59:50.349Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2024-11-11 22:59:50 2024-11-11T21:59:50.349Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.31]
2024-11-11 22:59:50 2024-11-11T21:59:50.408Z  INFO 1 --- [snow-peak-server] [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2024-11-11 22:59:50 2024-11-11T21:59:50.411Z  INFO 1 --- [snow-peak-server] [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 2787 ms
2024-11-11 22:59:50 2024-11-11T21:59:50.832Z  WARN 1 --- [snow-peak-server] [           main] com.zaxxer.hikari.HikariConfig           : HikariPool-1 - idleTimeout has been set but has no effect because the pool is operating as a fixed size pool.
2024-11-11 22:59:50 2024-11-11T21:59:50.834Z  INFO 1 --- [snow-peak-server] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2024-11-11 22:59:51 2024-11-11T21:59:51.907Z  WARN 1 --- [snow-peak-server] [           main] ConfigServletWebServerApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource [org/springframework/boot/autoconfigure/orm/jpa/HibernateJpaConfiguration.class]: Failed to initialize dependency 'flywayInitializer' of LoadTimeWeaverAware bean 'entityManagerFactory': Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:51 SQL State  : 08001
2024-11-11 22:59:51 Error Code : 0
2024-11-11 22:59:51 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51
2024-11-11 22:59:51 2024-11-11T21:59:51.912Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardService   : Stopping service [Tomcat]
2024-11-11 22:59:51 2024-11-11T21:59:51.935Z  INFO 1 --- [snow-peak-server] [           main] .s.b.a.l.ConditionEvaluationReportLogger :
2024-11-11 22:59:51
2024-11-11 22:59:51 Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2024-11-11 22:59:51 2024-11-11T21:59:51.970Z ERROR 1 --- [snow-peak-server] [           main] o.s.boot.SpringApplication               : Application run failed
2024-11-11 22:59:51
2024-11-11 22:59:51 org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource [org/springframework/boot/autoconfigure/orm/jpa/HibernateJpaConfiguration.class]: Failed to initialize dependency 'flywayInitializer' of LoadTimeWeaverAware bean 'entityManagerFactory': Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:51 SQL State  : 08001
2024-11-11 22:59:51 Error Code : 0
2024-11-11 22:59:51 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:326) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:205) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:954) ~[spring-context-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:625) ~[spring-context-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:146) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:754) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:456) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at org.springframework.boot.SpringApplication.run(SpringApplication.java:335) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at org.springframework.boot.SpringApplication.run(SpringApplication.java:1363) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at org.springframework.boot.SpringApplication.run(SpringApplication.java:1352) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at hu.snowpeak.server.SnowPeakServerApplication.main(SnowPeakServerApplication.java:10) ~[!/:0.0.1-SNAPSHOT]
2024-11-11 22:59:51 at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at java.base/java.lang.reflect.Method.invoke(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at org.springframework.boot.loader.launch.Launcher.launch(Launcher.java:102) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:51 at org.springframework.boot.loader.launch.Launcher.launch(Launcher.java:64) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:51 at org.springframework.boot.loader.launch.JarLauncher.main(JarLauncher.java:40) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:51 Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:51 SQL State  : 08001
2024-11-11 22:59:51 Error Code : 0
2024-11-11 22:59:51 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1806) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:600) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:522) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:337) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:335) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:200) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:313) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 ... 15 common frames omitted
2024-11-11 22:59:51 Caused by: org.flywaydb.core.internal.exception.FlywaySqlException: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:51 SQL State  : 08001
2024-11-11 22:59:51 Error Code : 0
2024-11-11 22:59:51 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51
2024-11-11 22:59:51 at org.flywaydb.core.internal.jdbc.JdbcUtils.openConnection(JdbcUtils.java:60) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:51 at org.flywaydb.core.internal.jdbc.JdbcConnectionFactory.<init>(JdbcConnectionFactory.java:72) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:51 at org.flywaydb.core.FlywayExecutor.execute(FlywayExecutor.java:134) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:51 at org.flywaydb.core.Flyway.migrate(Flyway.java:147) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:51 at org.springframework.boot.autoconfigure.flyway.FlywayMigrationInitializer.afterPropertiesSet(FlywayMigrationInitializer.java:66) ~[spring-boot-autoconfigure-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1853) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1802) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:51 ... 22 common frames omitted
2024-11-11 22:59:51 Caused by: org.postgresql.util.PSQLException: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:51 at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:352) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:54) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:273) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.Driver.makeConnection(Driver.java:446) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.Driver.connect(Driver.java:298) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at com.zaxxer.hikari.util.DriverDataSource.getConnection(DriverDataSource.java:137) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at com.zaxxer.hikari.pool.PoolBase.newConnection(PoolBase.java:360) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at com.zaxxer.hikari.pool.PoolBase.newPoolEntry(PoolBase.java:202) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:461) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at com.zaxxer.hikari.pool.HikariPool.checkFailFast(HikariPool.java:550) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at com.zaxxer.hikari.pool.HikariPool.<init>(HikariPool.java:98) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at com.zaxxer.hikari.HikariDataSource.getConnection(HikariDataSource.java:111) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:51 at org.flywaydb.core.internal.jdbc.JdbcUtils.openConnection(JdbcUtils.java:48) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:51 ... 28 common frames omitted
2024-11-11 22:59:51 Caused by: java.net.ConnectException: Connection refused
2024-11-11 22:59:51 at java.base/sun.nio.ch.Net.pollConnect(Native Method) ~[na:na]
2024-11-11 22:59:51 at java.base/sun.nio.ch.Net.pollConnectNow(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at java.base/sun.nio.ch.NioSocketImpl.timedFinishConnect(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at java.base/sun.nio.ch.NioSocketImpl.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at java.base/java.net.SocksSocketImpl.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at java.base/java.net.Socket.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:51 at org.postgresql.core.PGStream.createSocket(PGStream.java:260) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.core.PGStream.<init>(PGStream.java:121) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.core.v3.ConnectionFactoryImpl.tryConnect(ConnectionFactoryImpl.java:140) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:268) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:51 ... 40 common frames omitted
2024-11-11 22:59:51
2024-11-11 22:59:53
2024-11-11 22:59:53   .   ____          _            __ _ _
2024-11-11 22:59:53  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
2024-11-11 22:59:53 ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
2024-11-11 22:59:53  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
2024-11-11 22:59:53   '  |____| .__|_| |_|_| |_\__, | / / / /
2024-11-11 22:59:53  =========|_|==============|___/=/_/_/_/
2024-11-11 22:59:53
2024-11-11 22:59:53  :: Spring Boot ::                (v3.3.5)
2024-11-11 22:59:53
2024-11-11 22:59:54 2024-11-11T21:59:54.082Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : Starting SnowPeakServerApplication v0.0.1-SNAPSHOT using Java 21.0.5 with PID 1 (/opt/app/app.jar started by spring in /opt/app)
2024-11-11 22:59:54 2024-11-11T21:59:54.087Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : No active profile set, falling back to 1 default profile: "default"
2024-11-11 22:59:55 2024-11-11T21:59:55.516Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2024-11-11 22:59:55 2024-11-11T21:59:55.603Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 75 ms. Found 2 JPA repository interfaces.
2024-11-11 22:59:56 2024-11-11T21:59:56.553Z  INFO 1 --- [snow-peak-server] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8080 (http)
2024-11-11 22:59:56 2024-11-11T21:59:56.590Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2024-11-11 22:59:56 2024-11-11T21:59:56.590Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.31]
2024-11-11 22:59:56 2024-11-11T21:59:56.644Z  INFO 1 --- [snow-peak-server] [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2024-11-11 22:59:56 2024-11-11T21:59:56.647Z  INFO 1 --- [snow-peak-server] [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 2458 ms
2024-11-11 22:59:57 2024-11-11T21:59:57.044Z  WARN 1 --- [snow-peak-server] [           main] com.zaxxer.hikari.HikariConfig           : HikariPool-1 - idleTimeout has been set but has no effect because the pool is operating as a fixed size pool.
2024-11-11 22:59:57 2024-11-11T21:59:57.046Z  INFO 1 --- [snow-peak-server] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2024-11-11 22:59:58 2024-11-11T21:59:58.127Z  WARN 1 --- [snow-peak-server] [           main] ConfigServletWebServerApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource [org/springframework/boot/autoconfigure/orm/jpa/HibernateJpaConfiguration.class]: Failed to initialize dependency 'flywayInitializer' of LoadTimeWeaverAware bean 'entityManagerFactory': Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:58 SQL State  : 08001
2024-11-11 22:59:58 Error Code : 0
2024-11-11 22:59:58 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58
2024-11-11 22:59:58 2024-11-11T21:59:58.130Z  INFO 1 --- [snow-peak-server] [           main] o.apache.catalina.core.StandardService   : Stopping service [Tomcat]
2024-11-11 22:59:58 2024-11-11T21:59:58.148Z  INFO 1 --- [snow-peak-server] [           main] .s.b.a.l.ConditionEvaluationReportLogger :
2024-11-11 22:59:58
2024-11-11 22:59:58 Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2024-11-11 22:59:58 2024-11-11T21:59:58.174Z ERROR 1 --- [snow-peak-server] [           main] o.s.boot.SpringApplication               : Application run failed
2024-11-11 22:59:58
2024-11-11 22:59:58 org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource [org/springframework/boot/autoconfigure/orm/jpa/HibernateJpaConfiguration.class]: Failed to initialize dependency 'flywayInitializer' of LoadTimeWeaverAware bean 'entityManagerFactory': Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:58 SQL State  : 08001
2024-11-11 22:59:58 Error Code : 0
2024-11-11 22:59:58 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:326) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:205) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:954) ~[spring-context-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:625) ~[spring-context-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:146) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:754) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:456) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at org.springframework.boot.SpringApplication.run(SpringApplication.java:335) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at org.springframework.boot.SpringApplication.run(SpringApplication.java:1363) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at org.springframework.boot.SpringApplication.run(SpringApplication.java:1352) ~[spring-boot-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at hu.snowpeak.server.SnowPeakServerApplication.main(SnowPeakServerApplication.java:10) ~[!/:0.0.1-SNAPSHOT]
2024-11-11 22:59:58 at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at java.base/java.lang.reflect.Method.invoke(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at org.springframework.boot.loader.launch.Launcher.launch(Launcher.java:102) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:58 at org.springframework.boot.loader.launch.Launcher.launch(Launcher.java:64) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:58 at org.springframework.boot.loader.launch.JarLauncher.main(JarLauncher.java:40) ~[app.jar:0.0.1-SNAPSHOT]
2024-11-11 22:59:58 Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'flywayInitializer' defined in class path resource [org/springframework/boot/autoconfigure/flyway/FlywayAutoConfiguration$FlywayConfiguration.class]: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:58 SQL State  : 08001
2024-11-11 22:59:58 Error Code : 0
2024-11-11 22:59:58 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1806) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:600) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:522) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:337) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:335) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:200) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:313) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 ... 15 common frames omitted
2024-11-11 22:59:58 Caused by: org.flywaydb.core.internal.exception.FlywaySqlException: Unable to obtain connection from database: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2024-11-11 22:59:58 SQL State  : 08001
2024-11-11 22:59:58 Error Code : 0
2024-11-11 22:59:58 Message    : Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58
2024-11-11 22:59:58 at org.flywaydb.core.internal.jdbc.JdbcUtils.openConnection(JdbcUtils.java:60) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:58 at org.flywaydb.core.internal.jdbc.JdbcConnectionFactory.<init>(JdbcConnectionFactory.java:72) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:58 at org.flywaydb.core.FlywayExecutor.execute(FlywayExecutor.java:134) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:58 at org.flywaydb.core.Flyway.migrate(Flyway.java:147) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:58 at org.springframework.boot.autoconfigure.flyway.FlywayMigrationInitializer.afterPropertiesSet(FlywayMigrationInitializer.java:66) ~[spring-boot-autoconfigure-3.3.5.jar!/:3.3.5]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1853) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1802) ~[spring-beans-6.1.14.jar!/:6.1.14]
2024-11-11 22:59:58 ... 22 common frames omitted
2024-11-11 22:59:58 Caused by: org.postgresql.util.PSQLException: Connection to localhost:5454 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
2024-11-11 22:59:58 at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:352) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:54) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:273) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.Driver.makeConnection(Driver.java:446) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.Driver.connect(Driver.java:298) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at com.zaxxer.hikari.util.DriverDataSource.getConnection(DriverDataSource.java:137) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at com.zaxxer.hikari.pool.PoolBase.newConnection(PoolBase.java:360) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at com.zaxxer.hikari.pool.PoolBase.newPoolEntry(PoolBase.java:202) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:461) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at com.zaxxer.hikari.pool.HikariPool.checkFailFast(HikariPool.java:550) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at com.zaxxer.hikari.pool.HikariPool.<init>(HikariPool.java:98) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at com.zaxxer.hikari.HikariDataSource.getConnection(HikariDataSource.java:111) ~[HikariCP-5.1.0.jar!/:na]
2024-11-11 22:59:58 at org.flywaydb.core.internal.jdbc.JdbcUtils.openConnection(JdbcUtils.java:48) ~[flyway-core-10.10.0.jar!/:na]
2024-11-11 22:59:58 ... 28 common frames omitted
2024-11-11 22:59:58 Caused by: java.net.ConnectException: Connection refused
2024-11-11 22:59:58 at java.base/sun.nio.ch.Net.pollConnect(Native Method) ~[na:na]
2024-11-11 22:59:58 at java.base/sun.nio.ch.Net.pollConnectNow(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at java.base/sun.nio.ch.NioSocketImpl.timedFinishConnect(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at java.base/sun.nio.ch.NioSocketImpl.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at java.base/java.net.SocksSocketImpl.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at java.base/java.net.Socket.connect(Unknown Source) ~[na:na]
2024-11-11 22:59:58 at org.postgresql.core.PGStream.createSocket(PGStream.java:260) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.core.PGStream.<init>(PGStream.java:121) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.core.v3.ConnectionFactoryImpl.tryConnect(ConnectionFactoryImpl.java:140) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:268) ~[postgresql-42.7.4.jar!/:42.7.4]
2024-11-11 22:59:58 ... 40 common frames omitted
2024-11-11 22:59:58
2024-11-11 23:00:00
2024-11-11 23:00:00   .   ____          _            __ _ _
2024-11-11 23:00:00  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
2024-11-11 23:00:00 ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
2024-11-11 23:00:00  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
2024-11-11 23:00:00   '  |____| .__|_| |_|_| |_\__, | / / / /
2024-11-11 23:00:00  =========|_|==============|___/=/_/_/_/
2024-11-11 23:00:00
2024-11-11 23:00:00  :: Spring Boot ::                (v3.3.5)
2024-11-11 23:00:00
2024-11-11 23:00:00 2024-11-11T22:00:00.267Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : Starting SnowPeakServerApplication v0.0.1-SNAPSHOT using Java 21.0.5 with PID 1 (/opt/app/app.jar started by spring in /opt/app)
2024-11-11 23:00:00 2024-11-11T22:00:00.272Z  INFO 1 --- [snow-peak-server] [           main] h.s.server.SnowPeakServerApplication     : No active profile set, falling back to 1 default profile: "default"
2024-11-11 23:00:01 2024-11-11T22:00:01.737Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2024-11-11 23:00:01 2024-11-11T22:00:01.846Z  INFO 1 --- [snow-peak-server] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 97 ms. Found 2 JPA repository interfaces.
