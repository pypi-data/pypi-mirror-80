# ci-cmg-cruise-schema-orm

## Setting Up a Virtual Environment with pyenv
```bash
pyenv virtualenv 2.7.18 cruise-schema-orm-2.7.18
pyenv local cruise-schema-orm-2.7.18
```

## Building
Since this project can use JDBC divers, Apache Maven is used to build and test the library.
Java 8+ and Maven must be installed and on the PATH.  JAVA_HOME and MAVEN_HOME
environment variables should be set.

This project uses a docker container running an Oracle database to run tests.  Docker must be installed.

The tests use the Oracle JDBC driver.  This driver is not available from the Maven central repository.  Download the 
driver from Oracle and either
host this in a remote private repository, or manually add it to your local repository.

To build and test, run the following from the root of the project:
```bash
mvn clean install
```