-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 25 mai 2025 à 17:22
-- Version du serveur : 11.7.2-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `voyages_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `voyages_depart`
--

CREATE TABLE `voyages_depart` (
  `id` bigint(20) NOT NULL,
  `date_depart` date NOT NULL,
  `disponibilites` int(10) UNSIGNED NOT NULL CHECK (`disponibilites` >= 0),
  `circuit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `voyages_depart`
--

INSERT INTO `voyages_depart` (`id`, `date_depart`, `disponibilites`, `circuit_id`) VALUES
(1, '2025-08-10', 10, 1),
(2, '2025-07-01', 15, 2),
(3, '2025-06-15', 20, 3),
(4, '2025-09-05', 25, 4),
(5, '2025-10-12', 18, 5),
(6, '2025-11-20', 12, 6);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `voyages_depart`
--
ALTER TABLE `voyages_depart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `voyages_depart_circuit_id_a9d726ad_fk_voyages_circuit_id` (`circuit_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `voyages_depart`
--
ALTER TABLE `voyages_depart`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `voyages_depart`
--
ALTER TABLE `voyages_depart`
  ADD CONSTRAINT `voyages_depart_circuit_id_a9d726ad_fk_voyages_circuit_id` FOREIGN KEY (`circuit_id`) REFERENCES `voyages_circuit` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
